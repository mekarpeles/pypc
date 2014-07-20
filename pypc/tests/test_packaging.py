#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    tests.test_packaging
    ~~~~~~~~~~~~~~~~~~~~

    This module tests the pypc packaging pipeline

    :copyright: (c) 2014 by Hackerlist.
    :license: BSD, see LICENSE for more details.
"""

import os
import unittest
from pypc.pypc import Package

VALID_PATH = os.path.expanduser('~')

ERR = {
    'invalid-basename': 'Package instantiation requires non-empty basename',
    'failed-instantiation': 'Package path incorrectly set'
}


class TestPackage(unittest.TestCase):

    def test_creation(self):
        self.assertRaises(TypeError, Package, '', ERR['invalid-basename'])
        p = Package(VALID_PATH)
        self.assertTrue(p.path == VALID_PATH, ERR['failed-instantiation'])

    def test_generation(self):
        """Generation (i.e. Package(PATH).new()) tests should use
        a tempfile directory path.
        """
        pass
