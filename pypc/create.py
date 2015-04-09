#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from .settings import DEFAULTS, setup_fs, setup_opts, header


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

    def __init__(self, pkgname, path=None, venv='venv'):
        """Assumes path of current working directory $PWD by default.
        >>> Package('pythagorean')
        """
        _path = path or os.getcwd()
        if not os.path.exists(_path):
            raise OSError('Valid existing path required')
        if not pkgname:
            raise TypeError("Path '%s' must include a basename" % _path)
        self.path = _path
        self.pkgname = pkgname
        self.venv = venv

    def as_package(func):
        """Decorator which preempts func by switching directories to
        the Package's local context (venv) prior to execution and then
        restores back to pypc's native context afterwards.
        """
        def switch_ctx(self, *args, **kwargs):
            """Allows Package methods to easily operate within /
            change paths by wrapping them with Context.
            """
            with Context(self.path):
                return func(self, *args, **kwargs)
        return switch_ctx

    def disallow_customfs(f):
        """Convenience decorator, raises exception if user attempts to
        provide custom `fs` before feature is implemented
        """
        def inner(self, *args, **kwargs):
            if kwargs.get('fs', None):
                raise NotImplementedError
            return f(self, *args, **kwargs)
        return inner

    def strict(f):
        """Decorates func with ability to install pip dependencies +
        setup virtuenv if strict-mode (--strict flag is present)
        """
        def inner(self, *args, **kwargs):
            res = f(self, *args, **kwargs)
            if kwargs.get('strict', False):
                self.install_virtualenv()
                print('\nTo activate virtualenv, run:')
                print('\n\t`source venv/bin/activate`\n')
                pkgs = kwargs.get('dependencies', {})
                self.install_requirements(pkgs=pkgs)
            return res
        return inner

    @strict
    @disallow_customfs
    def new(self, fs=None, **options):
        """Scaffolds a new package, creates the directory hierarchy
        """
        minimal = options.pop('minimal', False)
        opts = setup_opts(minimal=minimal, **options)
        _fs = fs or setup_fs(minimal=minimal, **opts)

        def buildfs(fs, path=""):
            """Recurses the filesystem `fs` dict and touches necessary
            files with appropriate contents
            """
            if type(fs) is not dict:
                return self.touch(fs, path, **opts)

            for f in fs:
                cwd = os.path.join(path, f.replace('$', self.pkgname))
                if type(fs[f]) is dict:
                    if not os.path.exists(cwd):
                        os.makedirs(cwd)
                    buildfs(fs[f], path=cwd)
                else:
                    self.touch(fs[f], path=cwd, **opts)
        return buildfs(fs=_fs, path=self.path)

    def touch(self, contents, path, **options):
        """Touches a file or resource named $fname into existence at
        location $path and fill it with $contents data as specified

        params:
            contents - contents of file to create
            path - current full path in fs tree
        """
        if contents and not os.path.exists(path):
            fname = path.rsplit(os.sep, 1)[-1]
            if fname.endswith(".py"):
                _header = header(
                    fname, options['desc'], options['author'],
                    options['python'], options['encoding']
                    )
                contents = _header + contents
            with open(path, 'w') as fout:
                fout.write(contents)

    @as_package
    def install_virtualenv(self):
        """Installs virtualenv system-wide and configures Package's
        virtual environment.
        """
        if not self.is_installed('virtualenv'):
            pip.main(['install', 'virtualenv'])
        venv = os.path.join(self.path, self.venv)
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
        with Context(path):
            pkgs = pip.get_installed_distributions()
            return sorted('%s==%s' % (p.key, p.version) for p in pkgs)

    def setup_virtualenv(self, name='venv'):
        """Performs the initial configuration and package environment setup"""
        try:
            WorkingSet().require('virtualenv')
        except DistributionNotFound:
            pip.main(['install', 'virtualenv'])
        self.activate_virtualenv(named=name)

    @as_package
    def activate_virtualenv(self, named):
        shell = os.environ["SHELL"]
        subprocess.Popen('mkvirtualenv %s' % named, executable=shell,
                         shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

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
