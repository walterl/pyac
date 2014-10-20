# -*- coding: utf-8 -*-

__author__ = 'Walter Leibbrandt'
__email__ = 'git wrl co za'
__version__ = '0.0.1'

__all__ = ['accesscontrol', 'ACL', 'AccessDeniedError']

from functools import wraps


def accesscontrol(check_fn):
    """Decorator for access controlled callables. In the example scenario where
        access control is based solely on user names (user objects are `str`),
        the following is an example usage of this decorator::

            @accesscontrol(lambda user: user == 'bob')
            def only_bob_can_call_this():
               pass

        Class methods are decorated in the same way.

        :param check_fn: A callable, taking a user object argument, and
            returning a boolean value, indicating whether the user (user object
            argument) is allowed access to the decorated callable."""
    if not callable(check_fn):
        raise TypeError(check_fn)

    def decorator(wrapped):
        @wraps(wrapped)
        def decorated(*args, **kwargs):
            if ACL.current_user is None:
                raise AccessDeniedError(decorated)
            if not ACL.managed_funcs[decorated](ACL.current_user):
                raise AccessDeniedError(decorated)
            return wrapped(*args, **kwargs)

        ACL.managed_funcs[decorated] = check_fn
        return decorated

    return decorator


class ACL(object):
    """Access control list. This class cannot be instantiated, but is used as a
        namespace to store ACL-related data. It provides the
        :func:`ACL.for_user()` class method that allows client code to call
        access controlled callables."""
    current_user = None
    managed_funcs = dict()

    def __init__(self):
        raise TypeError('This class cannot be instantiated')

    @classmethod
    def for_user(cls, user):
        """Creates an access control context bound to the given user object.
            The returned context is necessary to call any access controlled
            callables. Example::
                @accesscontrol(lambda user: user.name == 'bob')
                def access_controlled_func():
                    pass

                with ACL.for_user(users.load('bob')):
                    access_controlled_func()"""
        return ACLContext(user)


class ACLContext(object):
    """Access control context. This context manager should not be instantiated
        directly, but through :meth:`ACL.for_user()`."""
    def __init__(self, user):
        self.user = user

    def __enter__(self):
        ACL.current_user = self.user

    def __exit__(self, exctype, excvalue, trackback):
        ACL.current_user = None


class AccessDeniedError(Exception):
    """Raised when an access controlled callable is called without an access
        control context of an allowed user. It contains two attributes:

         * `func`: The callable to which access was denied. Note that this will
           be a function object for methods (not bound or unbound methods),
           because of the way the callables are decorated.
         * `user`: The user (from the access control context) that attempted to
           call the access controlled callable, and for whom access was denied.
           If an access controlled callable is called outside of an access
           control context, this value will be `None`."""
    def __init__(self, func):
        self.func = func
        self.user = ACL.current_user
        msg = 'func={} user={}'.format(func.__name__, self.user)
        super(AccessDeniedError, self).__init__(msg)
