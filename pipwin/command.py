# -*- coding: utf-8 -*-
"""pipwin installs compiled python binaries on windows provided by Christoph
Gohlke

Usage:
  pipwin install <package> [-r=<file> | --file=<file>]
  pipwin uninstall <package>
  pipwin download <package> [-d=<dest> | --dest=<dest>] [-r=<file> | --file=<file>]
  pipwin search <package>
  pipwin list
  pipwin refresh
  pipwin (-h | --help)
  pipwin (-v | --version)

Options:
  -h --help     Show this screen.
  --version     Show version.
  -r=<file> --file=<file>  File with list of package names.
  -d=<dest> --dest=<dest>  Download packages into <dest>.
"""

from docopt import docopt
import sys
import platform
from warnings import warn
from . import pipwin
from packaging.requirements import Requirement


def _package_names(args):
    if args["--file"]:
        with open(args["--file"], 'r') as fid:
            for package in fid.readlines():
                if package and not package.startswith('#'):
                    yield Requirement(package.strip())
    elif not args["<package>"]:
        print("Provide a package name")
        sys.exit(0)
    else:
        yield Requirement(args["<package>"])
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

    args = docopt(__doc__, version="pipwin v0.4.1")

    # Warn if not on windows
    if platform.system() != "Windows":
        warn("Found a non Windows system. Package installation might not work.")

    # Handle refresh
    if args["refresh"]:
        pipwin.refresh()
        sys.exit(0)

    cache = pipwin.PipwinCache()

    # Handle list
    if args["list"]:
        cache.print_list()
        sys.exit(0)

    for package in _package_names(args):
        exact_match, matches = cache.search(package)
        if not exact_match:
            _print_unresolved_match_msg(package, matches)
            sys.exit(0)
        print("Package `{}` found in cache".format(package))
        # Handle install/uninstall/download
        if args["install"]:
            cache.install(package)
        elif args["uninstall"]:
            cache.uninstall(package)
        elif args["download"]:
            cache.download(package, dest=args["--dest"])
