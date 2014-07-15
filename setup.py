#-*- coding: utf-8 -*-

"""
pypc
----

Pypc is a tool for creating Python Packages. 

Generating a Project
````````````````````

.. code:: bash

    $ pypc create helloworld

Setup
`````

.. code:: bash

    $ pip install pypc
    $ ls
    LICENSE pypc/ README requirements.txt setup.py

Links
`````

* `website <http://github.com/mekarpeles/pypc/>`_

"""

from __future__ import print_function
from setuptools import Command, setup
import os

setup(
    name='pypc',
    version='0.1.1-dev',
    url='http://github.com/mekarpeles/pypc',
    author='hackerlist',
    author_email='m@hackerlist.net',
    packages=[
        'pypc',
        'pypc/tests'
        ],
    platforms='any',
    license='LICENSE',
    install_requires=[
    ],
    scripts=[
        "scripts/pypc"
        ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        ],
    description="Python3 Package Creator",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
)
