#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import getpass
from . import __title__, __version__, Package


def argparser():
    """Creates a command line ArgumentParser for pypc.

    re: `fs`, It would be nice to collect analytics on how often `fs`
    is req'd.  Cookiecutter + Donald Stufft lead me to believe often
    see: groups.google.com/forum/#!topic/pypa-dev/eaku1xvUVHU
    """
    parser = argparse.ArgumentParser(description=__title__)
    parser.add_argument('-v', help="Displays the pypc version",
                        action="version", version="%s v%s"
                        % (__title__, __version__))
    parser.add_argument('-m', '--minimal', dest="minimal",
                        help="Minimal mode, setup.py only",
                        action="store_true")
    parser.add_argument('-s', '--strict', dest="strict",
                        help="Install linters, virtualenv",
                        action="store_true")
    parser.add_argument('--cli', dest="cli", help="Create cli script",
                        default=None)
    parser.add_argument('--venv', dest="venv", help="Virtualenv dirname",
                        default='venv')
    parser.add_argument(dest="pkgname", help="Desired package name")
    parser.add_argument('--path', dest="path",
                        help="Path to package directory")
    parser.add_argument('--author', dest="author", help="Author's name",
                        default=getpass.getuser())
    parser.add_argument('--email', dest="email", help="Author's email",
                        default='')
    parser.add_argument('-V', '--ver', dest="version",
                        help="Your package's version: defaults to v0.0.1"
                        "(use -V for pypc version)", default='0.0.1')
    parser.add_argument('--desc', dest="desc", help="Package desc",
                        default='no description available')
    parser.add_argument('--url', dest="url", help="Package url",
                        default='')
    parser.add_argument('--rm', dest="readme", help="README filename",
                        default='README.rst')
    parser.add_argument('--fs', dest="fs", help=".json File Structure",
                        default=None)
    return parser


def optparser(args):
    """Constructs a dictionary of settings from the values the user
    provides to the ArgumentParser. Used in Package.new() and for
    """
    return {
        'cli': args.cli,
        'venv': args.venv,
        'minimal': args.minimal,
        'strict': args.strict,
        'pkgname': args.pkgname,
        'author': args.author,
        'email': args.email,
        'version': args.version,
        'classifiers': [],
        'url': args.url,
        'desc': args.desc,
        'readme': args.readme,
        }


def main():
    parser = argparser()
    args = parser.parse_args()
    opts = optparser(args)
    pkg = Package(args.pkgname, path=args.path, venv=args.venv)
    pkg.new(**opts)


if __name__ == "__main__":
    main()
