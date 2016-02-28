====
pypc
====

|Build Status| |Wheel Status|

The Python3 Package Creator.

Pypc is a standard project generator for Python packages.

How it Works
============

Pypc is similar to yoeman in that it is a tool for generating project scaffolding. The pypc project aspires to integrate with the Python Packaging Authority `pip` tool to provide users with a standard, sane approach to creating python packages (via a command such as `pip create <package>`. Currently, pypc works similarly to git and will populate your current directory with the appropriate project files.

Installation
============

    $ pip install pypc

Usage
=====

Pypc helps you create the basic structure of your python
package. It uses the conventions and file structure outlined in
https://packaging.python.org/en/latest/distributing.html. Advanced options
exist for additionally automatically setting up virtualenv for your project,
pip install dependencies and linters, such as pyflakes and pep8, auto-generating
a pip freeze as requirements.txt, and creating command line entry points for your package.

The most basic example is `pypc <package-name>` which will populate your current working directory with
the correct project files. E.g:

    $ pypc project && ls
    
    CHANGES  docs/  examples/  LICENSE  MANIFEST.in  project/  README.md  setup.py  tox.in

Pypc also offers a -m or --minimal flag for purists who wish to generate only the minimal requirements. This
only creates a README and setup.py and does not require network access
(after pypc is installed).

    # Minimal install

    $ pypc -m project && ls

    project/  MANIFEST.in  README.rst  setup.py setup.cfg

In both cases, a project/ subdirectory is populated with an __init__.py.

Finally, pypc provides a --strict or -s mode which not only scaffolds your
project directory but additionally installs and activates
virtualenv and linters within your environment. Strict mode may be combined
with minimal mode:

    $ pypc -sm project

Options
=======

    usage: pypc [-h] [-v] [-m] [-s] [--venv VENV] [--path PATH] [--author AUTHOR]
                [--email EMAIL] [-V VERSION] [--desc DESC] [--url URL]
                [--rm README] [--fs FS]
                pkgname

If you only want to create a package with a setup.py (no virtual env,
etc), use the -m or --minimal flag.

Note: -v outputs the version of pypc whereas -V or --version is used to
 specify the initial version of the package you are creating. This is
 slightly confusion, and improvements are welcome.

Library
=======
Pypc can be imported and used as library.

    >>> from pypc.create import Package
    >>> p = Package("pkgname", path="~/optional") # defaults to os.getcwd()
    >>> p.new(**{'readme': 'README.md'}) # see pypc.settings.DEFAULTS for a list of default options (key,vals)

Philosopy
=========
* KISS. Small and simple enough (i.e. Flask/webpy, not django) that it can be integrated into pip,
* Defaults. a default modus of operandi which works offline,
* PEP 20. "There should be one-- and preferably only one --obvious way to do it." In this respect, the general file structure should remain static and accept overrides/overloading of templates and if specific modules/packages (like flask) require specific (additional) file structure, a builder can import/bootstrap using pypc (as it would pip)

Standards
=========
Resources about the standards and walkthroughs:

* http://guide.python-distribute.org/creation.html
* http://www.scotttorborg.com/python-packaging/minimal.html
* http://stackoverflow.com/questions/9411494/how-do-i-create-a-pip-installable-project
* http://docs.python-guide.org/en/latest/writing/structure/
* http://www.kennethreitz.org/essays/repository-structure-and-python
* http://as.ynchrono.us/2007/12/filesystem-structure-of-python-project_21.html
* http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/

Alternatives
============
* https://github.com/audreyr/cookiecutter
* https://github.com/seanfisk/python-project-template - Git based, clone repo (requires altering git history)

Questions for you
=================
1) Does the file structure pypc generates break any conventions?
2) Is the code for pypc readable/accessible?
3) Feature suggestions? (would love to auto-init venv)

Disclaimer
==========
Pypc is a pre-alpha proof of concept. It's slow as it installs pyflakes, pep8, virtualenv sets up a virtualenv, and then generates a freeze list of requirements).
Right now there is little to no test-coverage; being it is a proof of concept, I'll try to continue as TDD.

Discussion
==========
Join the conversation! Other design considerations and details can be found on the pypa mailing list: https://groups.google.com/forum/#!searchin/pypa-dev/mek/pypa-dev/eaku1xvUVHU/Kbj_17sP23kJ

.. |Build Status| image:: https://travis-ci.org/mekarpeles/pypc.png

.. |Wheel Status| image:: https://pypip.in/wheel/pypc/badge.svg
    :target: https://pypi.python.org/pypi/pypc/
    :alt: Wheel Status
