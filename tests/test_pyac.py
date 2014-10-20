#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyac
---------

Functional tests for pyac - Python Access Control.
"""

import unittest

from pyac import ACL, accesscontrol


class TestPyac(unittest.TestCase):

    def test_pyac_registers_functions(self):
        @accesscontrol(lambda user: True)
        def show():
            print 'Shows the wiki page'

        @accesscontrol(lambda user: user.is_admin)
        def edit():
            print 'Edit the wiki page'

        self.assertIn(show, ACL.managed_funcs)
        self.assertIn(edit, ACL.managed_funcs)


if __name__ == '__main__':
    unittest.main()
