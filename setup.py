#!/usr/bin/env python

# PyPI supports rST, hence:
__doc__ = """\
`prelogging` streamlines the configuration of Python logging, provides
better error checking, and offers easy multiprocessing-safe
logging to streams, files, rotating files and the system log.
"""
from prelogging import __version__, __author__
from setuptools import setup    #, find_packages

setup(
    name='prelogging',
    version=__version__,
    author=__author__,       # "Brian O'Neill",
    author_email='twangist@gmail.com',
    description='streamlines the configuration of Python logging, includes '
                'multiprocessing-safe handlers',
    long_description=__doc__,
    license='MIT',
    keywords='logging config dictConfig dict configuration multiprocessing '
             'rotating file syslog SMTP queue handler',
    url='http://github.com/Twangist/prelogging',
    packages=['prelogging'],
    test_suite='run_tests.py',
    scripts=[],
    include_package_data=False,
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Topic :: System :: Logging',
    ]
)
