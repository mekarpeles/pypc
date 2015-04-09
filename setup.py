#-*- coding: utf-8 -*-

"""
pypc
----

Pypc is a tool for creating Python Packages. 

Generating a Project
````````````````````

.. code:: bash

    $ pypc helloworld

Setup
`````

.. code:: bash

    $ pip install pypc
    $ pypc helloworld

    AUTHORS CHANGES docs/ examples/ LICENSE MANIFEST.in project/ README.md requirements.txt setup.py tox.in venv/

Links
`````

* `website <http://github.com/mekarpeles/pypc/>`_

"""

import codecs
import os
import re
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    """Taken from pypa pip setup.py:
    intentionally *not* adding an encoding option to open, See:
       https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    """
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='pypc',
    version=find_version("pypc", "__init__.py"),
    description="Python3 Package Creator",
    long_description=read('README.rst'),
    author='Mek Karpeles',
    author_email='michael.karpeles@gmail.com',
    url='http://github.com/mekarpeles/pypc',
    packages=[
        'pypc',
        'pypc/templates'
        ],
    platforms='any',
    include_package_data=True,
    license='LICENSE',
    install_requires=[
        'jinja2',
        'argparse',
        'flake8',
        'pyflakes',
        'virtualenv'
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
        "Programming Language :: Python :: 3.4"
        ],
    entry_points={
        'console_scripts': ['pypc=pypc.cli:main'],
        }
)
