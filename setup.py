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

from setuptools import setup
import os

setup(
    name='pypc',
    version='0.1.3',
    url='http://github.com/mekarpeles/pypc',
    author='hackerlist',
    author_email='m@hackerlist.net',
    packages=[
        'pypc',
        'pypc/tests',
        'pypc/templates'
        ],
    platforms='any',
    include_package_data=True,
    license='LICENSE',
    install_requires=[
        'argparse == 1.2.1',
        'pep8 == 1.5.7',
        'pyflakes == 0.8.1',
        'flake8 == 2.2.2',
        'virtualenv == 1.11.6',
    ],
    scripts=[
        "scripts/pypc",
        ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3"
        "Programming Language :: Python :: 3.4"
        ],
    description="Python3 Package Creator",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
)
