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
