#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
     ____  _  _  ____   ___
    (  _ \( \/ )(  _ \ / __)
     ) __/ )  /  ) __/( (__
    (__)  (__/  (__)   \___)
    ~~~~~~~~~~~~~~~~~~~~~~~~

    pypc, the python package creator

    :copyright: (c) 2015 by Mek Karpeles.
    :license: see LICENSE for more details.
"""

__title__ = 'pypc'
__version__ = "0.1.5dev1"
__author__ = [
    "Mek <michael.karpeles@gmail.com>"
]

import sys
from .create import Package  # NOQA
from .settings import DEFAULTS  # NOQA
from .cli import main

if __name__ == '__main__':
    sys.exit(main())
