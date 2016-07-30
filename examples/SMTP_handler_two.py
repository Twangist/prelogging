#!/usr/bin/env python

__author__ = 'brianoneill'

import logging

try:
    import lcd
except ImportError:
    import sys
    sys.path[0:0] = ['..']          # , '../..'
from lcd import LoggingConfigDictEx


#
# NOTE: EDIT THESE TWO VARIABLES to try this example
#
SMTP_USERNAME = 'john.doe'      # assuming your sending email address is 'john.doe@gmail.com'
SMTP_PASSWORD = 'password'      # your gmail password
#
# AND THESE TWO TOO if necessary
#
FROM_ADDRESS =  SMTP_USERNAME + '@gmail.com'
SMTP_SERVER = 'smtp.gmail.com'

# for testing/trying it the example
TEST_TO_ADDRESS = FROM_ADDRESS


def add_smtp_handler_to_lcd(
                     lcdx,          # *
                     handler_name,
                     level,
                     toaddrs,        # string or list of strings
                     subject,
                     filters=()):
    """Factor out calls to ``add_smtp_handler``.
    """
    lcdx.add_smtp_handler(
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


def configure_logging():
    lcdx = LoggingConfigDictEx(attach_handlers_to_root=True)
    lcdx.add_stderr_console_handler('con-err', formatter='level_msg')
    # root, console handler levels: WARNING.

    # Add TWO SMTPHandlers, one for each level ERROR and CRITICAL,
    #    which will email technical staff with logged messages of levels >= ERROR.
    # We use a filter to make the first handler squelch CRITICAL messages:
    lcdx.add_function_filter("filter-error-only", filter_error_only)

    # TEST_TO_ADDRESS included just for testing/trying out the example
    basic_toaddrs = [TEST_TO_ADDRESS, 'problems@kludge.ly']

    # add error-only SMTP handler
    add_smtp_handler_to_lcd(
                     lcdx,
                     'email-error',
                     level='ERROR',
                     toaddrs=basic_toaddrs,
                     subject='ERROR (Alert from SMTPHandler)',
                     filters=['filter-error-only'])
    # add critical-only SMTP handler
    add_smtp_handler_to_lcd(
                     lcdx,
                     'email-critical',
                     level='CRITICAL',
                     toaddrs=basic_toaddrs + ['cto@kludge.ly'],
                     subject='CRITICAL (Alert from SMTPHandler)')
    lcdx.dump()
    lcdx.config()

# -----------------------------------------

def main():
    configure_logging()

    root = logging.getLogger()
    root.warning("Be careful")                  # logged to console
    root.error("Something bad just happened")   # logged to console, emailed
    root.critical("Time to restart")            # ditto


if __name__ == '__main__':
    main()

