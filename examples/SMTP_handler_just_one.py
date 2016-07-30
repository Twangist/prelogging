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


def main():
    # root, console handler levels: WARNING.
    lcdx = LoggingConfigDictEx(attach_handlers_to_root=True)
    lcdx.add_stderr_console_handler('con-err',
                                    formatter='minimal'
    ).add_smtp_handler('email-handler',
        level='ERROR',
        formatter='time_logger_level_msg',
        # SMTPHandler-specific kwargs:
        mailhost='smtp.gmail.com',
        fromaddr=FROM_ADDRESS,
        toaddrs=[TEST_TO_ADDRESS, 'uh.oh@kludge.ly'], # string or list of strings
        subject='Alert from SMTPHandler',
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
       timeout=1.0
    )

    lcdx.config()

    root = logging.getLogger()
    root.debug("1.")        # not logged (loglevel too low)
    root.info("2.")         # ditto
    root.warning("3.")      # logged to console
    root.error("4.")        # logged to console, emailed
    root.critical("5.")     # ditto


if __name__ == '__main__':
    main()

