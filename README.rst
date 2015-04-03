====
pypc
====

The Python3 Package Creator.

Pypc generates standard scaffolding and environment for a Python package.
# Creates the directory structure show above in `Usage`
# Installs virtualenv + creates venv directory
# Installs pyflakes, pep8 to venv

Installation
============

    $ pip install pypc

Usage
=====
How do I create a pip python package?

    $ pypc project
    
    $ cd project;ls

    AUTHORS  CHANGES  docs/  examples/  LICENSE  MANIFEST.in  project/  README.md  requirements.txt  setup.py  tox.in  venv/


Options
=======

    usage: pypc [-h] [--author AUTHOR] [--email EMAIL] [--version VERSION]
                [--desc DESC] [--url URL]
                path

Philosopy
=========
# KISS. Small and simple enough (i.e. Flask/webpy, not django) that it can be integrated into pip,
# Defaults. a default modus of operandi which works offline,
# PEP 20. "There should be one-- and preferably only one --obvious way to do it." In this respect, the general file structure should remain static and accept overrides/overloading of templates and if specific modules/packages (like flask) require specific (additional) file structure, a builder can import/bootstrap using pypc (as it would pip)

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

.. |Build Status| image:: https://travis-ci.org/mekarpeles/pypc.png
