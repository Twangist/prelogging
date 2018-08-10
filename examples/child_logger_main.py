#!/usr/bin/env python

__doc__ = """
Create a nonroot logger with two child loggers, one propagating and one not.
The parent logger has a stderr handler and a file handler, shared by the
propagating logger. The nonpropagating logger creates its own stderr handler
by cloning its parent's stderr handler; however, it uses the same file handler
as its parent (and by its sibling).

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

import examples.child_logger_sub_noprop as sub_noprop
import examples.child_logger_sub_prop as sub_prop


LOG_PATH = '_log/child_loggers/'
SHARED_FILE_HANDLER_NAME = 'app_file'

def config_logging(logfilename):
    lcd = init_logging_config(__name__, logfilename)
    sub_noprop.logging_config_sub(lcd, __name__,
                                  file_handler=SHARED_FILE_HANDLER_NAME)
    sub_prop.logging_config_sub(lcd, __name__)
    lcd.config()


def init_logging_config(loggername, logfilename):
    # add handlers to root == False (default)
    lcd = LCDict(log_path=LOG_PATH)

    # Create stderr console handler; output shows logger name and loglevel;
    ## loglevel higher than DEBUG.
    lcd.add_formatter('busier_console_fmt',
                      format='%(name)-40s: %(levelname)-8s: %(message)s'
    ).add_stderr_handler('console',
                         formatter='busier_console_fmt',
                         level='INFO'
    )
    # Add main file handler, which will write to LOG_PATH + '/' + logfilename,
    # and add logger (loggername == __name__) that uses it
    lcd.add_formatter('my_file_formatter',
                      format='%(name)-40s: %(levelname)-8s: '
                             '%(asctime)24s: %(message)s'
    ).add_file_handler('app_file',
                       filename=logfilename,
                       mode='w',
                       level='DEBUG',
                       formatter='my_file_formatter'
    ).add_logger(loggername,
                 handlers=('app_file', 'console'),
                 level='DEBUG',
                 propagate=False    # so it DOESN'T propagate to parent logger
    )
    return lcd

def boring(n):
    logging.getLogger(__name__).debug("Doing something boring with %d" % n)
    sub_noprop.do_something_boring(n)
    sub_prop.do_something_boring(n)

def special(n):
    logging.getLogger(__name__).info("Doing something special with %d" % n)
    sub_noprop.do_something_special(n)
    sub_prop.do_something_special(n)


def main():
    config_logging('child_loggers.log')

    logging.getLogger(__name__).info("Starting up... ")

    for i in range(3):
        boring(i)
        special(i)

    logging.getLogger(__name__).info("... shutting down.")


if __name__ == '__main__':
    main()

    # Written to stderr -- something like this (but flush left)::
    '''
    __main__                 : INFO    : Starting up...
    __main__.sub_noprop      : DEBUG   : Doing something boring with 0
    __main__                 : INFO    : Doing something special with 0
    __main__.sub_noprop      : INFO    : Doing something SPECIAL with 0
    __main__.sub_prop        : INFO    : Doing something SPECIAL with 0
    __main__.sub_noprop      : DEBUG   : Doing something boring with 1
    __main__                 : INFO    : Doing something special with 1
    __main__.sub_noprop      : INFO    : Doing something SPECIAL with 1
    __main__.sub_prop        : INFO    : Doing something SPECIAL with 1
    __main__.sub_noprop      : DEBUG   : Doing something boring with 2
    __main__                 : INFO    : Doing something special with 2
    __main__.sub_noprop      : INFO    : Doing something SPECIAL with 2
    __main__.sub_prop        : INFO    : Doing something SPECIAL with 2
    __main__                 : INFO    : ... shutting down.
    '''
    # Written to _log/child_loggers/child_loggers.log (flush left):
    '''
    __main__                 : INFO    :  2016-07-07 15:23:53,424: Starting up...
    __main__                 : DEBUG   :  2016-07-07 15:23:53,424: Doing something boring with 0
    __main__.sub_noprop      : DEBUG   :  2016-07-07 15:23:53,424: Doing something boring with 0
    __main__.sub_prop        : DEBUG   :  2016-07-07 15:23:53,424: Doing something boring with 0
    __main__                 : INFO    :  2016-07-07 15:23:53,424: Doing something special with 0
    __main__.sub_noprop      : INFO    :  2016-07-07 15:23:53,424: Doing something SPECIAL with 0
    __main__.sub_prop        : INFO    :  2016-07-07 15:23:53,425: Doing something SPECIAL with 0
    __main__                 : DEBUG   :  2016-07-07 15:23:53,425: Doing something boring with 1
    __main__.sub_noprop      : DEBUG   :  2016-07-07 15:23:53,425: Doing something boring with 1
    __main__.sub_prop        : DEBUG   :  2016-07-07 15:23:53,425: Doing something boring with 1
    __main__                 : INFO    :  2016-07-07 15:23:53,425: Doing something special with 1
    __main__.sub_noprop      : INFO    :  2016-07-07 15:23:53,425: Doing something SPECIAL with 1
    __main__.sub_prop        : INFO    :  2016-07-07 15:23:53,425: Doing something SPECIAL with 1
    __main__                 : DEBUG   :  2016-07-07 15:23:53,425: Doing something boring with 2
    __main__.sub_noprop      : DEBUG   :  2016-07-07 15:23:53,425: Doing something boring with 2
    __main__.sub_prop        : DEBUG   :  2016-07-07 15:23:53,425: Doing something boring with 2
    __main__                 : INFO    :  2016-07-07 15:23:53,425: Doing something special with 2
    __main__.sub_noprop      : INFO    :  2016-07-07 15:23:53,425: Doing something SPECIAL with 2
    __main__.sub_prop        : INFO    :  2016-07-07 15:23:53,425: Doing something SPECIAL with 2
    __main__                 : INFO    :  2016-07-07 15:23:53,426: ... shutting down.
    '''
