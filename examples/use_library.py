#!/usr/bin/env python

__author__ = 'brianoneill'

import library

import logging

try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['..']          # , '../..'
from prelogging import LCDict


def logging_config():
    d = LCDict(attach_handlers_to_root=True)  # LCDict default: =False
    d.add_stdout_handler('stdout', formatter='logger_level_msg', level='DEBUG')
    # NOTE: root level is WARNING (default),
    #  .    'library' logger level is INFO.
    #  .    Messages of 'library' propagate,
    #  .        and those of levels INFO and up *are logged*.
    d.config()


def main():
    # Exercise:
    # Comment out and uncomment the following two lines, individually
    # (4 cases); observe the console output in each case.

    logging_config()
    logging.getLogger().warning("I must caution you about that.")

    library.do_package_thing()
    library.do_something()
    library.do_something_else()

    # Results:
    """
    (1)
            logging_config()
            logging.getLogger().warning("I must caution you about that.")
      writes to stdout:
            root                : WARNING : I must caution you about that.
            library             : INFO    : INFO msg from package logger
            Did package thing.
            library.module      : INFO    : INFO msg
            Did something.
            library.module.other: WARNING : WARNING msg
            Did something else.
    (2)
            # logging_config()
            logging.getLogger().warning("I must caution you about that.")

      writes (to stdout)
            Did package thing.
            Did something.
            Did something else.
      and (to stderr)
          I must caution you about that.
      (possibly between or after the lines written to stdout).

    (3)
            logging_config()
            # logging.getLogger().warning("I must caution you about that.")
      writes to stdout:
            library             : INFO    : INFO msg from package logger
            Did package thing.
            library.module      : INFO    : INFO msg
            Did something.
            library.module.other: WARNING : WARNING msg
            Did something else.
    (4)
            # logging_config()
            # logging.getLogger().warning("I must caution you about that.")
      writes to stdout
            Did package thing.
            Did something.
            Did something else.
    """


if __name__ == '__main__':
    main()
