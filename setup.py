#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.test import test as TestCommand

import pyac


class NoseTestCommand(TestCommand):
    # This command was taken from
    # https://fgimian.github.io/blog/2014/04/27/running-nose-tests-with-plugins-using-the-python-setuptools-test-command/
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import nose
        nose.run_exit(argv=['nosetests'])


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = []

test_requirements = ['nose', 'coverage']

description = ('A simple, function level, back-end agnostic access control '
               'mechanism.')

setup(
    name='pyac',
    version=pyac.__version__,
    description=description,
    long_description=readme + '\n\n' + history,
    author='Walter Leibbrandt',
    author_email='git wrl co za',
    url='https://github.com/walterl/pyac',
    packages=['pyac'],
    package_dir={'pyac': 'pyac'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='pyac',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'nosetest': NoseTestCommand}
)
