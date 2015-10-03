# -*- coding: utf-8 -*-

import pip
import requests
from bs4 import BeautifulSoup
from os.path import expanduser, join, isfile, exists
import os
import json
import struct
from sys import version_info
from itertools import product
import pyprind

MAIN_URL = "http://www.lfd.uci.edu/~gohlke/pythonlibs/"
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}

def parse_url(ml, mi):
    """
    Parse url from ml and mi component of the link.
    This works according to the js functions on the website.
    The functions are reproduced here:

    function dl1(ml,mi){
        var ot="";
        for(var j=0;j<mi.length;j++)
            ot+=String.fromCharCode(ml[mi.charCodeAt(j)-48]);
        location.href=ot;
    }
    function dl(ml,mi){
        mi=mi.replace('&lt;','<');
        mi=mi.replace('&gt;','>');
        mi=mi.replace('&amp;','&');
        setTimeout(function(){dl1(ml,mi)},1500);
    }
    """

    # Reform >, < and &
    mi = mi.replace("&lt;", "<")
    mi = mi.replace("&gt;", ">")
    mi = mi.replace("&amp;", "&")

    route = "";
    for character in mi:
        route += chr(ml[ord(character) - 48])

    return MAIN_URL + route

def build_cache():
    """
    Get current data from the website http://www.lfd.uci.edu/~gohlke/pythonlibs/

    Returns
    -------
    Dictionary containing package details
    """

    data = {}

    req = requests.get(MAIN_URL, headers=HEADER)
    soup = BeautifulSoup(req.text)
    links = soup.find(class_="pylibs").find_all("a")
    for link in links:
        if link.get("onclick") is not None:
            jsfun = link.get("onclick").split("\"")
            mlstr = jsfun[0].split("(")[1].strip()[1:-2]
            ml = map(int, mlstr.split(","))
            mi = jsfun[1]
            url = parse_url(ml, mi)

            # Details = [package, version, pyversion, --, arch]
            details = url.split("/")[-1].split("-")
            details[0] = details[0].lower().replace("_", "-")

            # Not using EXEs and ZIPs
            if len(details) != 5:
                continue
            # arch = win32 / win_amd64 / any
            arch = details[4]
            arch = arch.split(".")[0]
            # ver = cpXX / pyX / pyXX
            ver = details[2]
            if data.has_key(details[0]):
                data[details[0]].update({ver + "-" + arch: url})
            else:
                data[details[0]] = {ver + "-" + arch: url}

    return data


def filter_packages(data):
    """
    Filter packages based on your current system
    """

    sys_data = {}

    # Check lists
    verlist = []
    archlist = []
    ver = version_info[:2]
    verlist.append("cp" + str(ver[0]) + str(ver[1]))
    verlist.append("py" + str(ver[0]))
    verlist.append("py" + str(ver[0]) + str(ver[1]))
    verlist.append("py2.py3")

    archlist.append("any")
    if (struct.calcsize("P") * 8) == 32:
        archlist.append("win32")
    elif (struct.calcsize("P") * 8) == 64:
        archlist.append("win_amd64")

    checklist = map("-".join, list(product(verlist, archlist)))

    for key in data.keys():
        presence = map(data[key].has_key, checklist)
        try:
            id = presence.index(True)
        except ValueError:
            # Version not found
            continue
        sys_data[key] = data[key][checklist[id]]

    return sys_data


class PipwinCache(object):
    """
    Pipwin cache class
    """

    def __init__(self, refresh=False):
        """
        Search if cache file is there in HOME.
        If not, build one.

        Parameters
        ----------
        refresh: boolean
            If True, rebuilds the cache.
        """

        home_dir = expanduser("~")
        self.cache_file = join(home_dir, ".pipwin")

        if isfile(self.cache_file) and not refresh:
            with open(self.cache_file, "rb") as fp:
                self.data = json.load(fp)
        else:
            print("Building cache. Hang on . . .")
            self.data = build_cache()

            with open(self.cache_file, "wb") as fp:
                json.dump(self.data, fp,
                          sort_keys=True,
                          indent=4,
                          separators=(",", ": "))

        if not refresh:
            # Create a package list for the system
            self.sys_data = filter_packages(self.data)

    def print_list(self):
        """
        Print the list of packages available for system
        """

        print("Listing packages available for your system\n")
        for package in self.sys_data.keys():
            print " -> " + package

    def search(self, package):
        """
        Search for a package

        Returns
        -------
        exact_match : boolean
            True if exact match is found
        matches : list
            List of matches. Is a string if exact_match is True.
        """

        exact_match = package in self.sys_data.keys()

        if exact_match:
            return [exact_match, package]

        found = []
        for pack in self.sys_data.keys():
            if package in pack:
                # Partial string search
                found.append(pack)

        return [exact_match, found]

    def install(self, package):
        """
        Install a package
        """

        print ("Downloading package")
        url = self.sys_data[package]
        wheel_name = url.split("/")[-1]

        home_dir = expanduser("~")
        pipwin_dir = join(home_dir, "pipwin")

        if not exists(pipwin_dir):
            os.makedirs(pipwin_dir)

        wheel_file = join(pipwin_dir, wheel_name)

        res = requests.get(url, headers=HEADER, stream=True)
        length = res.headers.get("content-length")
        chunk = 1024

        bar = pyprind.ProgBar(int(length) / chunk)
        if int(length) < chunk:
            bar = None

        wheel_handle = open(wheel_file, "wb")
        for block in res.iter_content(chunk_size=chunk):
            wheel_handle.write(block)
            wheel_handle.flush()
            if bar is not None:
                bar.update()
        wheel_handle.close()

        pip.main(["install", wheel_file])

        os.remove(wheel_file)

    def uninstall(self, package):
        """
        Uninstall a package
        """

        pip.main(["uninstall", self.sys_data[package]])


def refresh():
    """
    Rebuild the cache
    """

    PipwinCache(refresh=True)
