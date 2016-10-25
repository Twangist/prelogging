#!/usr/bin/env python

__doc__ = """
Give the root logger a stderr handler and a file handler. Create two loggers,
one propagating and the other not. The nonpropagating logger creates its own
stderr handler by cloning the root's stderr handler; however, it uses the same
file handler used by the root (and by its sibling).

Observe how the loglevels of the handlers and loggers determine what gets written
to the two destinations.
"""
__author__ = 'brianoneill'

import os
import time
import math
import logging

try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['..']
from prelogging import LCDict

import examples.child_logger2_sub_noprop as sub_noprop
import examples.child_logger2_sub_prop as sub_prop


LOG_PATH = '_log/child_loggers2/'


def config_logging(logfilename):
    lcd = init_logging_config(logfilename)
    sub_noprop.logging_config_sub(lcd)
    sub_prop.logging_config_sub(lcd)

    lcd.config()


def init_logging_config(logfilename):

    lcd = LCDict(log_path=LOG_PATH, attach_handlers_to_root=True)
    lcd.set_root_level('DEBUG')

    # Set format of console handler to show logger name and loglevel.
    ## Make sure 'console' handler level is higher than DEBUG
    lcd.add_formatter('busier_console_fmt',
                      format='%(name)-34s: %(levelname)-8s: %(message)s'
    ).add_stderr_handler('console',
                         formatter='busier_console_fmt',
                         level='INFO'
    )
    # Add main file handler that writes to '_log/child_loggers2/' + logfilename,
    # and add a logger that uses it
    lcd.add_formatter(
        'my_file_formatter',
        format='%(name)-34s: %(levelname)-8s: %(asctime)24s: %(message)s'
    ).add_file_handler(
        'app_file',
        filename=logfilename,
        mode='w',
        level='DEBUG',
        formatter='my_file_formatter'
    )
    return lcd

def report_name_package():
    logging.getLogger().info("__name__ = %r    __package__ = %r"
                             % (__name__, __package__))
    sub_noprop.report_name_package()
    sub_prop.report_name_package()

def boring(n):
    logging.getLogger().debug("Doing something boring with %d" % n)
    sub_noprop.do_something_boring(n)
    sub_prop.do_something_boring(n)

def special(n):
    logging.getLogger().warning("Doing something special with %d" % n)
    sub_noprop.do_something_special(n)
    sub_prop.do_something_special(n)


def main():
    config_logging('child_loggers2.log')

    logging.getLogger().info("Starting up... ")

    # report_name_package()

    for i in range(2):
        boring(i)
        special(i)

    logging.getLogger().info("... shutting down.")

# Written to stderr:
'''
root                              : INFO    : Starting up...
examples.child_logger2_sub_noprop : DEBUG   : Doing something boring with 0
root                              : WARNING : Doing something special with 0
examples.child_logger2_sub_noprop : INFO    : Doing something SPECIAL with 0
examples.child_logger2_sub_prop   : INFO    : Doing something SPECIAL with 0
examples.child_logger2_sub_noprop : DEBUG   : Doing something boring with 1
root                              : WARNING : Doing something special with 1
examples.child_logger2_sub_noprop : INFO    : Doing something SPECIAL with 1
examples.child_logger2_sub_prop   : INFO    : Doing something SPECIAL with 1
root                              : INFO    : ... shutting down.
'''

if __name__ == '__main__':
    main()
