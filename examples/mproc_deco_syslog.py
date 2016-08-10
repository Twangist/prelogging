#!/usr/bin/env python

__author__ = 'brianoneill'
__version__ = '0.2'

from deco import *
import time
import random
from collections import defaultdict
import logging

try:
    import lcd
except ImportError:
    import sys
    sys.path[0:0] = ['..', '../..']
from lcd import LCDEx

from examples._get_locking_pref import get_locking_pref

# LOGFILENAME = 'rot_fh.log'

#############################################################################

@concurrent(processes=3)    # the concurrent function
def process_x_y(x, y, data):
    time.sleep(0.1)

    logging.getLogger().warning("x, y = %d, %d"
                                "\n\t            that's  %d, %d"
                                % (x, y, x, y)
                               )
    return data[x + y]


@synchronized               # the function that calls the concurrent function
def process_data_set(data):

    results = defaultdict(dict)

    for x in range(3):
        for y in range(4):
            logging.getLogger().warning("x, y = %d, %d" % (x, y))
            results[x][y] = process_x_y(x, y, data)

    return dict(results)


def config_logging(use_locking):

    print("%s locking" % ("Using" if use_locking else "NOT using"))

    lcd_ex = LCDEx(root_level='DEBUG',
                   attach_handlers_to_root=True,
                   locking=use_locking)
    # Set up console handler to show process name, time, handler name
    lcd_ex.add_stderr_handler(
        'console', formatter='process_level_msg'
    )
    # Add syslog handler with same formatter
    lcd_ex.add_syslog_handler(
        'h_syslog',
        formatter='process_level_msg',
        address='/var/run/syslog',      # works for OS X; '/dev/log' for *nix
    )
    lcd_ex.check()
    lcd_ex.config()


def main(use_locking=None):
    """
    :param use_locking: bool
    :return:
    """
    if use_locking is None:
        use_locking = get_locking_pref()

    config_logging(use_locking)

    random.seed(0)
    data = [random.random() for _ in range(200)]
    start = time.time()
    logging.getLogger().info(process_data_set(data))
    logging.getLogger().info(time.time() - start)


#############################################################################

if __name__ == "__main__":
    main(False)
