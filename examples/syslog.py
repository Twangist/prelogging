#!/usr/bin/env python
"""
NON-multiprocessing rotating file handler.
"""

__author__ = 'brianoneill'

import logging
# from pprint import pformat

try:
    import logging_config
except ImportError:
    import sys
    sys.path[0:0] = ['../..']
from logging_config import LCDict


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
    lcd = LCDict(attach_handlers_to_root=True,
                 locking=True,
                 root_level='DEBUG')

    lcd.add_stdout_handler('console', formatter='msg')

    if not sys.platform.startswith('darwin'):
        raise NotImplementedError(
            "This example is currently implemented only for OS X / macOS")

    # add a syslog handler
    lcd.add_syslog_handler(
        'h_syslog',
        formatter='logger_level_msg',
        address='/var/run/syslog',
    )
    lcd.config()

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
