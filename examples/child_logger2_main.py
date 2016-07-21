#!/usr/bin/env python

__author__ = 'brianoneill'

import os
import time
import math
import logging

try:
    import lcd
except ImportError:
    import sys
    sys.path[0:0] = ['..']
from lcd import LoggingConfigDictEx

import examples.child_logger2_sub_noprop as sub_noprop
import examples.child_logger2_sub_prop as sub_prop


LOG_PATH = '_log/child_loggers2/'


def config_logging(logfilename):
    lcd_ex = init_logging_config(logfilename)
    sub_noprop.logging_config_sub(lcd_ex)
    sub_prop.logging_config_sub(lcd_ex)

    lcd_ex.config()


def init_logging_config(logfilename):

    lcd_ex = LoggingConfigDictEx(log_path=LOG_PATH,
                                 add_handlers_to_root=True)
    lcd_ex.set_root_level('DEBUG')

    # Change format of console handler to show logger `name` and loglevel `levelname`.
    ## Make sure 'console' handler level is higher than DEBUG
    lcd_ex.add_formatter('busier_console_fmt',
                         format='%(name)-34s: %(levelname)-8s: %(message)s')
    lcd_ex.add_stderr_console_handler('console',
                                      formatter='busier_console_fmt',
                                      level='INFO')

    # Add main file handler, which will write to '_log/child_loggers/' + logfilename,
    # and add logger that uses it
    lcd_ex.add_formatter(
        'my_file_formatter',
        format='%(name)-34s: %(levelname)-8s: %(asctime)24s: %(message)s'
    ).add_file_handler(
        'app_file',
        filename=logfilename,
        level='DEBUG',
        formatter='my_file_formatter'
    )
    return lcd_ex

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
