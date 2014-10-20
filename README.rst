====
PyAC
====

.. image:: https://badge.fury.io/py/pyac.png
    :target: http://badge.fury.io/py/pyac

.. image:: https://travis-ci.org/walterl/pyac.png?branch=master
        :target: https://travis-ci.org/walterl/pyac

.. image:: https://pypip.in/d/pyac/badge.png
        :target: https://pypi.python.org/pypi/pyac


A simple, function level, back-end agnostic access control mechanism.

* Free software: BSD license
* Documentation: http://pyac.readthedocs.org.

Features
--------

* TODO

Example
-------

    from pyac import accesscontrol

    class WikiPage(object):

        @accesscontrol(lambda user: True)
        def show(self):
            print('Stub: show wiki page')

        @accesscontrol(lambda user: user.is_admin)
        def edit(self):
            print('Stub: edit wiki page')

    ...

    wikipage = WikiPage()
    with ACL(user=users.load('normaluser')):
        wikipage.show()

        # Raises AccessDeniedError
        wikipage.edit()

    ...

    with ACL(user=users.load('admin')):
        wikipage.edit()
