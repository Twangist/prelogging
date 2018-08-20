#!/usr/bin/env python

__author__ = 'brianoneill'

import logging

try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['..']          # , '../..'
from prelogging import LCDict

from ._smtp_credentials import *

# for testing/trying it the example
TEST_TO_ADDRESS = FROM_ADDRESS


def add_smtp_handler_to_lcd(
                     lcd,          # *
                     handler_name,
                     level,
                     toaddrs,        # string or list of strings
                     subject,
                     filters=()):
    """Factor out calls to ``add_email_handler``.
    """
    lcd.add_email_handler(
        handler_name,
        level=level,
        filters=filters,

        toaddrs=toaddrs,
        subject=subject,

        formatter='time_logger_level_msg',
        fromaddr=FROM_ADDRESS,
        mailhost=SMTP_SERVER,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD
    )

def filter_error_only(record):
    "Let only ERROR messages through"
    return record.levelname  == 'ERROR'


def logging_config():
    lcd = LCDict(attach_handlers_to_root=True)
    # root level: WARNING
    lcd.add_stderr_handler('con-err', formatter='level_msg')
    # console handler level: NOTSET

    # Add TWO SMTPHandlers, one for each level ERROR and CRITICAL,
    #    which will email technical staff with logged messages of levels >= ERROR.
    # We use a filter to make the first handler squelch CRITICAL messages:
    lcd.add_callable_filter("filter-error-only", filter_error_only)

    # TEST_TO_ADDRESS included just for testing/trying out the example
    basic_toaddrs = [TEST_TO_ADDRESS, 'admin@kludge.ly']

    # add error-only SMTP handler
    add_smtp_handler_to_lcd(
                     lcd,
                     'email-error',
                     level='ERROR',
                     toaddrs=basic_toaddrs,
                     subject='ERROR (Alert from SMTPHandler)',
                     filters=['filter-error-only'])
    # add critical-only SMTP handler
    add_smtp_handler_to_lcd(
                     lcd,
                     'email-critical',
                     level='CRITICAL',
                     toaddrs=basic_toaddrs + ['cto@kludge.ly'],
                     subject='CRITICAL (Alert from SMTPHandler)')
    lcd.config()

# -----------------------------------------

def main():
    logging_config()

    root = logging.getLogger()
    root.warning("Be careful")                  # logged to console
    root.error("Something bad just happened")   # logged to console, emailed
    root.critical("Time to restart")            # ditto


if __name__ == '__main__':
    main()

