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
import subprocess
from settings import DEPENDENCIES, ROOT


class Context(object):
    """Switches a scope's context so that it's temporarily run within
    a specified path.

    usage:
        >>> with Context('/tmp/foo') as ctx:
        ...     print("helloworld from /tmp/foo")
    """

    def __init__(self, path, back=None):
        """Context stores a path to enter and a path to return to
        after it falls outside of scope
        """
        self.back = back or os.getcwd()
        self.forward = path

    def __enter__(self):
        os.chdir(self.forward)
        return self

    def __exit__(self, type_, value, traceback):
        os.chdir(self.back)


class Package(object):
    """A class which offers utilities for generating and maintaining
    python packages (across multiple python versions)
    """

    def __init__(self, path, venv='venv'):
        """
        >>> Package('/home/mek/pythagorean')
        >>> Package('pythagorean')
        """
        self.venv = venv
        self.path = path
        self.dirname, self.app = os.path.split(path)
        if not self.app:
            raise TypeError("Path '%s' must include a basename" % self.path)

    def as_package(func):
        """Decorator which preempts func by switching directories to
        the Package's local context (venv) prior to execution and then
        restores back to pypc's native context afterwards.
        """
        def switch_ctx(self, *args, **kwargs):
            """Allows Package methods to easily operate within / change paths by
            wrapping them with Context.
            """
            with Context(self.path):
                return func(self, *args, **kwargs)
        return switch_ctx

    def new(self, **kwargs):
        """Generates a new package, creates the directory hierarchy"""
        dirs = [d.replace('$', self.app) for d in ROOT['dirs']] + \
            kwargs.get('dirs', [])
        files = [f.replace('$', self.app) for f in ROOT['files']] + \
            kwargs.get('files', [])

        for d in dirs:
            try:
                os.makedirs(os.path.join(self.path, d))
            except OSError:
                print("Skipping '%s', dir exists." % d)

        for f in files:
            with open(os.path.join(self.path, f), 'wb'):
                pass

    @as_package
    def install_virtualenv(self):
        """Installs virtualenv system-wide and configures Package's
        virtual environment.
        """
        if not self.is_installed('virtualenv'):
            pip.main(['install', 'virtualenv'])
        venv = os.path.join(self.path,  self.venv)
        virtualenv.create_environment(venv)

    @as_package
    def as_venv(self, cmd=None):
        """Runs bash cmds within the virtualenv context

        usage:
            >>> p = Package('/tmp/foo')
            >>> p.new()
            >>> p.as_venv('pip freeze')
        """
        activate = '. %s' % os.path.join(self.venv, 'bin', 'activate')
        command = '%s && %s' % (activate, cmd) if cmd else activate
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        return proc.communicate()[0]

    @as_package
    def install_requirements(self, pkgs=None):
        """Installs default dependencies + user specified pkgs and
        then populates a requirements.txt.
        """
        pkgs = pkgs or []
        for d in DEPENDENCIES:
            self.as_venv('pip install %s' % d)

        with open(os.path.join(self.path, 'requirements.txt'), 'wb') as f:
            f.write(self.as_venv('pip freeze > requirements.txt'))

    @staticmethod
    def is_installed(key):
        """Determines of a package name is installed. It is
        recommended this method be run within a context decorated by
        @as_package.
        """
        return key in [d.key for d in pip.get_installed_distributions()]


if __name__ == "__main__":
    pass
