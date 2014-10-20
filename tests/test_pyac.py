#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyac
---------

Functional tests for pyac - Python Access Control.
"""

from __future__ import print_function

import unittest

from pyac import ACL, accesscontrol


class TestPyac(unittest.TestCase):

    def test_pyac_registers_functions(self):
        @accesscontrol(lambda user: True)
        def show():
            print('Shows the wiki page')

        @accesscontrol(lambda user: user.is_admin)
        def edit():
            print('Edit the wiki page')

        self.assertIn(show, ACL.managed_funcs)
        self.assertIn(edit, ACL.managed_funcs)

    def test_pyac_registers_methods(self):
        class WikiPage(object):

            @accesscontrol(lambda user: True)
            def show():
                print('Shows the wiki page')

            @accesscontrol(lambda user: user.is_admin)
            def edit():
                print('Edit the wiki page')

        self.assertIn(WikiPage.__dict__['show'], ACL.managed_funcs)
        self.assertIn(WikiPage.__dict__['edit'], ACL.managed_funcs)

    def test_pyac_registers_func_with_associated_checker(self):
        checker = lambda user: True

        @accesscontrol(checker)
        def show():
            print('Show wiki page')

        self.assertIs(ACL.managed_funcs[show], checker)

    def test_pyac_raises_TypeError_for_nonfunc_checker(self):
        with self.assertRaises(TypeError):
            @accesscontrol(None)
            def show():
                pass


if __name__ == '__main__':
    unittest.main()
