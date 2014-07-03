#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    template.py
    ~~~~~~~~~~~
    
    Static template for generating pkg scaffolding.

    :copyright: (c) 2014 by Mek.
    :license: GPLv3, see LICENSE for more details.
"""

from datetime import date

setup = """#!/usr/bin/env python
#-*- coding: utf-8 -*-

\"\"\"
    setup.py
    ~~~~~~~~

    Setup and installation for the {pkg} package.

    Install with:
    $ sudo pip install .

    :copyright: (c) {year} by {author}.
    :license: {license}, see LICENSE for more details.
\"\"\"

from distutils.core import setup
import os

setup(
    name='{pkg}',
    version='{version}',
    url='{url}',
    author='{author}',
    author_email='{email}',
    packages=[
        '{pkg}',
        ],
    platforms={platforms},
    license='LICENSE',
    install_requires={dependencies}
    description="{description}",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
)
"""

init = """#!/usr/bin/env python
#-*- coding: utf-8 -*-

\"\"\"
    setup.py
    ~~~~~~~~

    Setup and installation for the {pkg} package.

    Install with:
    $ sudo pip install .

    :copyright: (c) {year} by {author}.
    :license: {license}, see LICENSE for more details.
\"\"\"

__version__ = {version}

def get_version():
    \"\"\"Returns a PEP 386-compliant version number from VERSION.\"\"\"
    pass
"""
