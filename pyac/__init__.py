# -*- coding: utf-8 -*-

__author__ = 'Walter Leibbrandt'
__email__ = 'git wrl co za'
__version__ = '0.0.1'

from functools import wraps


def accesscontrol(check_fn):
    if not callable(check_fn):
        raise TypeError(check_fn)

    def decorator(wrapped):
        @wraps(wrapped)
        def decorated(*args, **kwargs):
            if not ACL.managed_funcs[decorated](ACL.current_user):
                raise AccessDeniedError()
            return wrapped(*args, **kwargs)

        ACL.managed_funcs[decorated] = check_fn
        return decorated

    return decorator


class AccessDeniedError(Exception):
    pass


class ACL(object):
    current_user = None
    managed_funcs = dict()

    def __init__(self):
        raise TypeError('This class cannot be instantiated')

    @classmethod
    def for_user(cls, user):
        return ACLContext(user)


class ACLContext(object):
    def __init__(self, user):
        self.user = user

    def __enter__(self):
        ACL.current_user = self.user

    def __exit__(self, exctype, excvalue, trackback):
        ACL.current_user = None
