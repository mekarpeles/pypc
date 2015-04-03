#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    pypc
    ~~~~

    This module creates new pypc packages

    :copyright: (c) 2015 by Mek Karpeles.
    :license: see LICENSE for more details.
"""

import os
import pip
import virtualenv
import subprocess
from pkg_resources import WorkingSet, DistributionNotFound
from .settings import DEFAULTS, header

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

    def __init__(self, path, **options):
        """
        >>> Package('/home/mek/pythagorean')
        >>> Package('pythagorean')
        """
        self.dirname, self.pkgname = os.path.split(path)
        self.path = path
        if not self.pkgname:
            raise TypeError("Path '%s' must include a basename" % self.path)

        for k in DEFAULTS.keys():
            if not hasattr(self, k):
                setattr(self, k, options.get(k, DEFAULTS[k]))

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

    def new(self):
        """Scaffolds a new package, creates the directory hierarchy
        """
        def buildfs(fs, path=""):   
            if type(fs) is not dict:
                return self.touch(fs, path)

            for f in fs:                
                cwd = "%s%s%s" % (path, os.sep, f.replace('$', self.pkgname))
                if type(fs[f]) is dict:
                    if not os.path.exists(cwd):
                        os.makedirs(cwd)
                    buildfs(fs[f], path=cwd)
                else:
                    self.touch(fs[f], cwd)
        return buildfs(fs=DEFAULTS['fs'](**self.__dict__), path=self.path)

    def touch(self, asset, path):
        """Touches a file or resource named $fname into existence at
        location $path and fills it with $asset data as specified"""
        if asset and not os.path.exists(path):
            fname = path.rsplit(os.sep, 1)[-1]
            if fname.endswith(".py"):
                asset = header(fname, self.desc, self.author,
                               self.encoding, self.python) + asset
            with open(path, 'w') as fout:
                fout.write(asset)

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
        for pkg in (pkgs or DEFAULTS['dependencies']):
            self.as_venv('pip install %s' % pkg)

        # record installed packages
        with open(os.path.join(self.path, 'requirements.txt'), 'wb') as f:
            f.write(self.as_venv('pip freeze > requirements.txt'))

    @staticmethod
    def is_installed(key):
        """Determines of a package name is installed. It is
        recommended this method be run within a context decorated by
        @as_package.
        """
        return key in [d.key for d in pip.get_installed_distributions()]


    def freeze(self):
        """Returns a list of modules installed for this Package"""
        self._freeze(self.path)

    @staticmethod
    def _freeze(path):
        """Generates a list of modules installed within path's local
        context, useful for generating requirements.txt
        
        TODO Consider using context manager instead of chdir
        see: http://stackoverflow.com/a/431747
        """
        with Context(path) as ctx:
            pkgs = pip.get_installed_distributions()
            return sorted('%s==%s' % (p.key, p.version) for p in pkgs)

    def setup_virtualenv(self, name='venv'):
        """Performs the initial configuration and package environment setup"""
        try:
            dep = WorkingSet().require('virtualenv')
        except DistributionNotFound:            
            pip.main(['install', 'virtualenv'])
        self.activate_virtualenv(named=name)

    @as_package
    def activate_virtualenv(self, named):
        shell = os.environ["SHELL"]
        subprocess.Popen('mkvirtualenv %s' % named, executable=shell, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #'workon %s' % named
        #'source %s/bin/activate' % named

    @as_package
    def install(self, dependencies=None):
        """Installs base dependencies and writes pip freeze to
        requirements.txt
        """
        for d in dependencies:
            pip.main(['install', d])
        with open('requirements.txt', 'wb') as f:
            requirements = '\n'.join(self.freeze())
            f.write(requirements)


if __name__ == "__main__":
    pass
