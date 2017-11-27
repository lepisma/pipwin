# -*- coding: utf-8 -*-

import argparse
import sys
import platform
from warnings import warn
from . import pipwin
from packaging.requirements import Requirement


def _package_names(args):
    if args.file:
        with open(args.file, 'r') as fid:
            for package in fid.readlines():
                if package and not package.startswith('#'):
                    yield Requirement(package.strip())
    elif not args.package:
        print("Provide a package name")
        sys.exit(0)
    else:
        yield Requirement(args.package)
    return


def _print_unresolved_match_msg(package, matches):
    if len(matches) > 0:
        print("Did you mean any of these ?\n")
        print(" * " + "\n * ".join(matches))
        print("")
    else:
        print("Package `{}` not found".format(package.name))
        print("Try `pipwin refresh`")

def main():
    """
    Command line entry point
    """

    parser = argparse.ArgumentParser(
        prog="pipwin",
        description="pipwin installs compiled python binaries on windows "
                    "provided by Christoph Gohlke")
    parser.add_argument("command",
                        choices=["install",
                                 "uninstall",
                                 "download",
                                 "search",
                                 "list",
                                 "refresh"],
                        help="the action to perform")
    parser.add_argument("package", nargs="?", help="the package name")
    parser.add_argument("-r", "--file", nargs="?", help="file with list of package names")

    args = parser.parse_args()

    # Warn if not on windows
    if platform.system() != "Windows":
        warn("Found a non Windows system. Package installation will not work.")

    # Handle refresh
    if args.command == "refresh":
        pipwin.refresh()
        sys.exit(0)

    cache = pipwin.PipwinCache()

    # Handle list
    if args.command == "list":
        cache.print_list()
        sys.exit(0)

    for package in _package_names(args):
        exact_match, matches = cache.search(package)
        if not exact_match:
            _print_unresolved_match_msg(package, matches)
            sys.exit(0)
        print("Package `{}` found in cache".format(package))
        # Handle install/uninstall/download
        if args.command == "install":
            cache.install(package)
        elif args.command == "uninstall":
            cache.uninstall(package)
        elif args.command == "download":
            cache.download(package)
