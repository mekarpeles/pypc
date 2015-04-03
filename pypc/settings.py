# -*- coding: utf-8 -*-
"""
    settings.py
    ~~~~~~~~~~~

    utilities for building files and setting default file values

    :copyright: (c) 2015 by Mek Karpeles.
    :license: see LICENSE for more details.
"""

import datetime
import textwrap
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('pypc', 'templates'))

def license(**options):
    return env.get_template('LICENSE').render()

def manifest(**options):
    return env.get_template('MANIFEST.in').render()

def setup(pkgname, version="", desc="", url="", author="", email="",
          dependencies=None, classifiers=None, **kwargs):
    """Generates a project's setup.py"""
    return env.get_template('setup.html').render(
        name=pkgname, version=version, url=url, author=author, email=email,
        desc=desc, dependencies=dependencies, classifiers=classifiers
        )

def changelog(version, **kwargs):
    """Generates a project's CHANGES changelog"""
    return env.get_template('CHANGES').render(
        version=version, date=datetime.datetime.now().ctime()
        )

def init(pkgname, version="", desc="", author="", **kwargs):
    """
    Generates a main __init__.py for the project w/ __version__, etc.

    usage:
        >>> init("python-mypkg", description="test desc", author="mek")
    """
    return env.get_template('__init__.py').render(
        title=pkgname, desc=desc, version=version, author=author
        )

def header(name, desc, author, python, encoding):
    """Creates headers for Python source files"""
    year = datetime.date.today().year + 1
    underline = len(name) * '~'
    desc = textwrap.fill(desc, width=79)
    return env.get_template('header.html').render(
        encoding=encoding, name=name, underline=underline, desc=desc,
        year=year, author=author
        )

DEFAULTS = {
    'pkgname': 'python-mypkg',
    'version': '0.0.1',
    'python': '3.4', #use env?
    'encoding': 'utf-8',
    'desc': '',
    'author': 'Anonymous',
    'email': '',
    'url': '',
    'dependencies': {
        'virtualenv': '1.11.6',
        'pep8': '1.5.7',
        'pyflakes': '0.8.1'
        },
    'classifiers': [],
    'venv': 'venv',
    'fs': lambda **options: {
        'docs': {},
        'examples': {},
        'AUTHORS': "",
        'CHANGES': changelog(**options),
        'LICENSE': license(**options),
        'MANIFEST.in': manifest(**options),
        'README.md': "",
        'tox.in': "",
        'setup.py': setup(**options),
        'Makefile': "",
        'tests': {
            "__init__.py": "", #todo
            },
        '$': { # pkg dir
            '__init__.py': init(**options),
            }
        }
    }

