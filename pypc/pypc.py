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
import pip
import virtualenv
from pkg_resources import WorkingSet, DistributionNotFound
from settings import DEPENDENCIES, ROOT, VERSION

class Context(object):

    def __init__(self, path, back=None):
        self.back = back or os.getcwd()
        self.forward = path

    def __enter__(self):
        os.chdir(self.forward)
        return self
        
    def __exit__(self, type, value, traceback):
        os.chdir(self.back)

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
            with Context(self.path):
                return func(self, *args, **kwargs)
        return switch_ctx

    def new(self, **kwargs):
        """Generate a new package"""
        dirs =  [d.replace('$', self.app) for d in ROOT['dirs' ]]
        files = [f.replace('$', self.app) for f in ROOT['files']]

        for d in dirs:
            try:                
                os.makedirs(os.path.join(self.path, d))
            except OSError:
                print("Skipping <%s>: dir exists." % d)

        for f in files:
            with open(os.path.join(self.path, f), 'wb') as t:
                pass

    @as_package
    def setup_virtualenv(self, name='venv'):
        """Installs and configures Package virtual environment"""
        try:
            dist = WorkingSet().require('virtualenv')
        except DistributionNotFound:            
            pip.main(['install', 'virtualenv'])

        virtualenv.create_environment(os.path.join(self.path, name))

if __name__ == "__main__":
    pass
