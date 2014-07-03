#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    test.py
    ~~~~~~~
    
    Test cases for gypy.

    :copyright: (c) 2014 by Mek.
    :license: GPLv3, see LICENSE for more details.
"""

import unittest
from template import setup, init

test_data = {
    'year': date.today().year,
    'pkg': 'gypy',
    'license': 'GPLv3',
    'author': 'Mek',
    'version': (0,0,0,0),
    'url': 'https://github.com/mekarpeles/gypy',
    'email': 'michael.karpeles@gmail.com',
    'platforms': 'all',
    'dependencies': [],
    'description': 'Generate Your Python (Project)'
 }

class TestGypy(unittest.TestCase):

    def test_setup(self):
        setup.format(**test)
