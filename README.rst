====
pypc
====

|Build Status|

The Python3 Package Creator

Installation
============

    $ pip install pypc

Usage
=====
How do I create a pip python package?

    $ pypc ~/project
    
    $ cd ~/project;ls

    AUTHORS  CHANGES  docs/  examples/  LICENSE  MANIFEST.in  project/  README.md  requirements.txt  setup.py  tox.in  venv/

Alternatives
============
* https://github.com/audreyr/cookiecutter
* https://github.com/seanfisk/python-project-template - Git based, clone repo (requires altering git history)

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

.. |Build Status| image:: https://travis-ci.org/mekarpeles/pypc.png
