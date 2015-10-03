# -*- coding: utf-8 -*-

import argparse
import sys
import platform
import pipwin

def main():
    """
    Command line entry point
    """

    parser = argparse.ArgumentParser(
        description="pipwin installs compiled python binaries on windows provided by Christoph Gohlke"
    )
    parser.add_argument("command",
                        choices=["install",
                                 "uninstall",
                                 "search",
                                 "list",
                                 "refresh"],
                        help="the action to perform")
    parser.add_argument("package",
                        nargs="?",
                        help="the package name")

    args = parser.parse_args()

    # Checking if not on Windows
    if platform.system() != "Windows":
        print("C'mon ! It's pip'win' ! Install it on a Windows machine.")
        sys.exit(0)

    # Setup cache and handle refresh
    if args.command == "refresh":
        pipwin.refresh()
        sys.exit(0)
    else:
        cache = pipwin.PipwinCache()

    # Handle list
    if args.command == "list":
        cache.print_list()
        sys.exit(0)
    elif not args.package:
        print("Provide a package name")
        sys.exit(0)

    # Search for package in cache
    exact_match, matches = cache.search(args.package)
    if exact_match:
        print("Package found in cache")
    else:
        if len(matches) > 0:
            print("Did you mean any of these ?\n")
            print(" * " + "\n * ".join(matches))
            print("")
        else:
            print("Package not found")
            print("Try `pipwin refresh`")
        sys.exit(0)

    # Handle install/uninstall
    if args.command == "install":
        cache.install(args.package)
    elif args.command == "uninstall":
        cache.uninstall(args.package)
