# -*- coding: utf-8 -*-

__author__ = 'Walter Leibbrandt'
__email__ = 'git wrl co za'
__version__ = '0.0.1'


def accesscontrol(check_fn):
    def decorator(wrapped):
        ACL.managed_funcs[wrapped] = check_fn
        return wrapped
    return decorator


class ACL(object):
    managed_funcs = dict()
