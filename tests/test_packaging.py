#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    tests.test_packaging
    ~~~~~~~~~~~~~~~~~~~~

    This module tests the pypc packaging pipeline

    :copyright: (c) 2014 by Hackerlist.
    :license: BSD, see LICENSE for more details.
"""

import sys
import os.path
import unittest

# Add pypc to the test path
p = os.path.abspath(
    os.path.join(os.path.join(
            os.path.dirname(__file__),
            os.path.pardir),
                 'pypc'))
sys.path.append(p)
    
import pypc

VALID_PATH = os.path.expanduser('~')

ERR = {
    'invalid-basename': 'Package instantiation requires non-empty basename',
    'failed-instantiation': 'Package path incorrectly set'
}


class TestPackage(unittest.TestCase):

    def test_creation(self):
        p = pypc.Package(VALID_PATH)
        self.assertTrue(p.path == VALID_PATH, ERR['failed-instantiation'])

    def test_generation(self):
        """Generation (i.e. Package(PATH).new()) tests should use
        a tempfile directory path.
        """
        pass
