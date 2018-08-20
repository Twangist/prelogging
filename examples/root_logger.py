#!/usr/bin/env python

__author__ = 'brianoneill'

import logging

try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['..']          # , '../..'
from prelogging import LCDict


#############################################################################

def config_logging(log_path, logfilename=''):
    """Create a root logger with a stdout console handler with loglevel=INFO,
    and, if logfilename is not empty, a file handler with default loglevel=NOTSET.
    Root loglevel will be INFO.
    """
    lcd = LCDict(log_path=log_path,
                 attach_handlers_to_root=True,
                 root_level='INFO')
    lcd.add_stdout_handler('console', level='INFO', formatter='msg')
    if logfilename:
        # add a file handler, which will write to log_path + '/' + logfilename
        lcd.add_formatter(
            'my_file_formatter',
            format='%(levelname)-8s: %(message)s',
        ).add_file_handler(
                'app_file',
                filename=logfilename,
                mode='w',
                formatter='my_file_formatter'
        )
    # lcd.dump()           # | DEBUG

    lcd.config()


def main():
    LOG_PATH = '_log/root_logger'       # NOTE: directory should already exist
    logfilename = 'logfile.log'

    config_logging(LOG_PATH, logfilename)

    logger = logging.getLogger()
    logger.debug("1. Message not logged")
    logger.warning("2. Log to both file and console")

    logger.setLevel(logging.DEBUG)
    logger.debug("3. Log to file only")
    logger.warning("4. Log to both file and console")

    # _log/root_logger/logfile.log contains these lines, flush left:
    #   WARNING : 2. Log to both file and console
    #   DEBUG   : 3. Log to file only
    #   WARNING : 4. Log to both file and console

    # Logged to the console (stdout), flush left:
    #   2. Log to both file and console
    #   4. Log to both file and console



#############################################################################

if __name__ == '__main__':
    main()
