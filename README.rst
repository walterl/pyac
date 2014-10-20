====
PyAC
====

Usage
-----

Add access control to functions and methods::

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

Call access controlled functions and methods::

    from pyac import ACL

    wikipage = WikiPage()

    with ACL.for_user(users.load('normaluser')):
        wikipage.show()
        wikipage.edit()  # Raises AccessDeniedError

    with ACL.for_user(users.load('admin')):
        wikipage.edit()

    with ACL.for_user(users.load('janitor')):
        cleanup_dead_links()
