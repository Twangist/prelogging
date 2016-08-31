#!/usr/bin/env python

# PyPI supports rST, hence:
__doc__ = """\
`logging_config` (for "logging config dict") streamlines the configuration of Python
logging, provides better error checking, and adds multiprocess-safe handlers
for writing to streams, files, rotating files and the system log.
"""
from logging_config import __version__, __author__
from setuptools import setup    #, find_packages

setup(
    name='logging_config',
    version=__version__,
    author=__author__,       # "Brian O'Neill",
    author_email='twangist@gmail.com',
    description='streamlines the configuration of Python logging, includes '
                'multiprocessing-safe handlers',
    long_description=__doc__,
    license='MIT',
    keywords='logging config dictConfig dict configuration multiprocessing '
             'rotating file syslog SMTP queue handler',
    url='http://github.com/Twangist/logging_config',
    packages=['logging_config'],
    test_suite='run_tests.py',
    scripts=[],
    include_package_data=False,     # ???
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Topic :: System :: Logging',
    ]
)
