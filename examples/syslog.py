#!/usr/bin/env python
"""
NON-multiprocessing rotating file handler.
"""

__author__ = 'brianoneill'

import logging
# from pprint import pformat

try:
    import lcd
except ImportError:
    import sys
    sys.path[0:0] = ['../..']
from lcd import LCDEx


# LOG_PATH = '_testlogs/rot_fh/'      # NOTE: directory must exist
# LOGFILENAME = 'test_rot_fh.log'

#############################################################################
import sys

def config_logging():
    """Create a root logger with a stdout console handler with level=WARNING,
    and a syslog handler with default level=NOTSET.
    Root logger level will be DEBUG.
    """
    # Defaults:
    #   attach_handlers_to_root=False,
    lcd_ex = LCDEx(attach_handlers_to_root=True,
                   # locking=True,
                   root_level='DEBUG')

    lcd_ex.add_stdout_handler('console', formatter='msg')

    platform = sys.platform
    if platform.startswith('darwin'):
        address = '/var/run/syslog'
    elif platform.startswith('linux'):
        address = '/dev/log'
    elif platform.startswith('win32'):
        raise NotImplementedError(
            "Figure out how to use the UDP option of SysLogHandler -- "
            "https://docs.python.org/3/library/logging.handlers.html#sysloghandler")
    else:
        raise NotImplementedError(
            "Don't know the correct address for SysLogHandler on OS = '%s' "
            "-- '/dev/log'?" % platform)

    # add a syslog handler
    lcd_ex.add_syslog_handler(
        'h_syslog',
        formatter='logger_level_msg',
        address=address
        # facility='local1'
    )
    # lcd_ex.dump()             # | DEBUG

    lcd_ex.config()

#############################################################################

def main():
    config_logging()
    logger = logging.getLogger()

    logger.debug("1 blah")
    logger.info("2 blah^2")
    logger.warning("3 Now is the time for the crazy brown fox to come to the aid of the party")
    logger.error("4 blah^4")
    logger.critical("5 blah^5")


if __name__ == '__main__':
    main()
