====
PyAC
====

This is very old code that I can only vaguely remember: today is
2019-04-13, and the previous commit was on 2014-10-20. This is only
published because it looks kinda cool. And the tests pass. :)

Based on the usage example below, it's a library for adding access
control to functions/methods. The access control is defined by arbitrary
callables that determine access for a given user. Those callables are
associated with the access controlled callable via the ``accesscontrol``
decorator.

In essence, it separates the access control logic from the code that is
access controlled.

The access control is then applied in the context of a specified user,
when the decorated callable is called. Decorated callables will raise
``AccessDeniedError`` when called without a user context.


Usage
-----

Add access control to functions and methods:

.. code-block:: python

    from pyac import accesscontrol

    class WikiPage(object):
        @accesscontrol(lambda user: True)
        def show(self):
            '''Any user may mall this method.'''
            print('Stub: show wiki page')

        @accesscontrol(lambda user: user.is_admin)
        def edit(self):
            '''Only admins may call this method.'''
            print('Stub: edit wiki page')

    @accesscontrol(lambda user: user.name == 'janitor')
    def cleanup_dead_links():
        '''Only callable by the "janitor" user.'''
        print('Stub: cleanup dead links in wiki')

Call access controlled functions and methods:

.. code-block:: python

    from pyac import ACL

    wikipage = WikiPage()

    with ACL.for_user(users.load('normaluser')):
        wikipage.show()
        wikipage.edit()  # Raises AccessDeniedError

    with ACL.for_user(users.load('admin')):
        wikipage.edit()

    with ACL.for_user(users.load('janitor')):
        cleanup_dead_links()
