#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    pypc
    ~~~~

    This module creates new pypc packages

    :copyright: (c) 2014 by Hackerlist.
    :license: BSD, see LICENSE for more details.
"""

import os

ROOT = {
    'dirs': [
        'docs', 'examples', '$/tests'
        ],
    'files': [
        'AUTHORS', 'CHANGES', 'LICENSE', 'MANIFEST.in', 'README.md', 'setup.py',
        'requirements.py', 'tox.in', '$/__init__.py', '$/tests/__init__.py'
        ]
    }

class Package(object):

    def __init__(self, path):
        """
        >>> Package('/home/mek/pythagorean')
        >>> Package('pythagorean')
        """
        self.path = path
        self.dirname, self.app = os.path.split(path)
        if not self.app:
            raise TypeError("Path <%s> must include a basename" % self.path)

    def as_package(func):
        """Decorator which preempts func by switching directories to
        the Package's local context (venv) prior to execution and then
        restores back to pypc's native context afterwards.
        """
        def switch_ctx(self, *args, **kwargs):
            os.chdir(self.path)
            ret = func(self, *args, **kwargs)
            os.chdir(self._path)
            return ret
        return switch_ctx

    def new(self, **kwargs):
        """Generate a new package"""
        dirs =  [d.replace('$', self.app) for d in ROOT['dirs' ]]
        files = [f.replace('$', self.app) for f in ROOT['files']]

        for d in dirs:
            try:
                os.makedirs('%s/%s' % (self.path, d))
            except OSError:
                print("Skipping <%s>: dir exists." % d)

        for f in files:
            with open('%s/%s' % (self.path, f), 'wb') as t:
                pass

if __name__ == "__main__":
    pass
