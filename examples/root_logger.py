#!/usr/bin/env python

__author__ = 'brianoneill'

import logging
from pprint import pformat

try:
    import lcd
except ImportError:
    import sys
    sys.path[0:0] = ['..']          # , '../..'
from lcd import LoggingConfigDictEx


#############################################################################

def config_logging(log_path, logfilename=''):
    """Create a root logger with a stdout console handler with level=INFO,
    and, if logfilename is not empty, a file handler with level=DEBUG.
    Root logger level will be INFO.
    """
    # Defaults:
    #   add_handlers_to_root=False,
    lcd_ex = LoggingConfigDictEx(log_path=log_path,
                                 add_handlers_to_root=True,
                                 root_level='INFO')
    lcd_ex.add_stdout_console_handler('console', formatter='minimal')
    # add a file handler, which will write to log_path + '/' + logfilename
    lcd_ex.add_formatter(
        'my_file_formatter',
        format='%(levelname)-8s: %(message)s',
    )
    if logfilename:
        lcd_ex.add_file_handler(
            'app_file',
            filename=logfilename,
            formatter='my_file_formatter',
        )
    # lcd_ex.dump()           # | DEBUG

    lcd_ex.config()


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