#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyac
---------

Functional tests for pyac - Python Access Control.
"""

from __future__ import print_function

import unittest

from pyac import accesscontrol, ACL, AccessDeniedError


class TestPyac(unittest.TestCase):

    def test_calling_func_in_acl_context_does_not_raise_for_valid_user(self):
        @accesscontrol(lambda user: user == 'bob')
        def show():
            pass

        try:
            with ACL.for_user('bob'):
                show()
        except AccessDeniedError as exc:
            self.fail(exc)

    def test_calling_func_in_acl_context_raises_for_invalid_user(self):
        @accesscontrol(lambda user: user == 'alice')
        def show():
            pass

        with ACL.for_user('bob'):
            with self.assertRaises(AccessDeniedError):
                show()

    def test_calling_method_in_acl_context_does_not_raise_for_valid_user(self):
        class WikiPage(object):
            @accesscontrol(lambda user: user == 'bob')
            def show(self):
                pass

        try:
            wikipage = WikiPage()
            with ACL.for_user('bob'):
                wikipage.show()
        except AccessDeniedError as exc:
            self.fail(exc)

    def test_calling_method_in_acl_context_raises_for_invalid_user(self):
        class WikiPage(object):
            @accesscontrol(lambda user: user == 'alice')
            def show(self):
                pass

        wikipage = WikiPage()
        with ACL.for_user('bob'):
            with self.assertRaises(AccessDeniedError):
                wikipage.show()

    def test_access_control_is_applied_to_different_funcs_in_one_context(self):
        class WikiPage(object):
            @accesscontrol(lambda user: True)
            def show(self):
                pass

            @accesscontrol(lambda user: user == 'admin')
            def edit(self):
                pass

        @accesscontrol(lambda user: False)
        def show():  # Forbidden show()
            pass

        wikipage = WikiPage()
        test_user = 'anonymous'
        with ACL.for_user(test_user):
            try:
                wikipage.show()
            except AccessDeniedError as exc:
                self.fail(exc)

            exc_regex = '^func={} user={}'.format(
                        WikiPage.edit.im_func.__name__, test_user)
            with self.assertRaisesRegexp(AccessDeniedError, exc_regex):
                wikipage.edit()

            exc_regex = '^func={} user={}'.format(show.__name__, test_user)
            with self.assertRaisesRegexp(AccessDeniedError, exc_regex):
                show()

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

    def test_pyac_raises_TypeError_for_noncallable_checker(self):
        with self.assertRaises(TypeError):
            @accesscontrol(None)
            def show():
                pass

    def test_pyac_raises_AccessDeniedError_on_func_call_if_check_fails(self):
        @accesscontrol(lambda user: False)
        def noone_may_call_this():
            pass

        with self.assertRaises(AccessDeniedError):
            noone_may_call_this()

    def test_acl_context_sets_current_user(self):
        with ACL.for_user('bob'):
            self.assertEqual(ACL.current_user, 'bob')

    def test_acl_cannot_be_instantiated(self):
        exc_regex = '^This class cannot be instantiated$'
        with self.assertRaisesRegexp(TypeError, exc_regex):
            ACL()

    def test_function_call_without_acl_context_raises_AccessDeniedError(self):
        @accesscontrol(lambda user: True)
        def show():
            pass

        exc_regex = '^func={} user={}'.format(show.__name__, None)
        with self.assertRaisesRegexp(AccessDeniedError, exc_regex):
            show()

    def test_AccessDeniedError_sets_fields_for_func_and_current_user(self):
        @accesscontrol(lambda user: False)
        def noone_may_call_this():
            pass

        try:
            with ACL.for_user('bob'):
                noone_may_call_this()
        except AccessDeniedError as exc:
            self.assertEqual(exc.user, 'bob')
            self.assertIs(exc.func, noone_may_call_this)


if __name__ == '__main__':
    unittest.main()
