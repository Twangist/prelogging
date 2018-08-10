#!/usr/bin/env python

__author__ = 'brianoneill'
__version__ = '0.2'

try:
    from deco import *
except ImportError:
    raise ImportError("`mproc_deco.py` requires the `deco` package -- "
                      "https://github.com/alex-sherman/deco")

import time
import random
from collections import defaultdict

import logging


try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['..']
from prelogging import LCDict

from examples._get_locking_pref import get_locking_pref


@concurrent     # add this for the concurrent function
def process_lat_lon(lat, lon, data):
    time.sleep(0.1)

    logging.getLogger().info("processing lat, lon = %d, %d"
                             "\n\t              %d, %d"
                             % (lat, lon, lat, lon)
                             # % (lat, lon)
                             )
    # logging.getLogger().debug('processing %d, %d' % (lat, lon))     # or use __name__

    return data[lat + lon]


@synchronized   # add this for the function that calls the concurrent function
def process_data_set(data):
    results = defaultdict(dict)
    for lat in range(5):
        for lon in range(5):
            logging.getLogger().info("lat, lon = %d, %d" % (lat, lon))

            results[lat][lon] = process_lat_lon(lat, lon, data)

    return dict(results)


def config_logging(use_locking):
    logfilename = 'logfile (%s).log' % ('LOCKING' if use_locking else 'NOLOCKING')
    lcd = LCDict(log_path='_log/mproc_deco/',
                 root_level='DEBUG',
                 attach_handlers_to_root=True,
                 locking=use_locking)
    # Set up console handler to show process name, time, handler name
    lcd.add_stderr_handler(
        'console', formatter='process_time_logger_level_msg', level='INFO'
    )
    # Add main file handler, which will write to log_path + '/' + logfilename
    lcd.add_file_handler(
        'app_file',
        filename=logfilename,
        mode='w',
        formatter='process_time_logger_level_msg',
    )
    lcd.config()


def main(use_locking=None):
    """
    :param use_locking: bool
    """
    if use_locking is None:
        use_locking = get_locking_pref()

    config_logging(use_locking)

    random.seed(0)
    data = [random.random() for _ in range(200)]
    start = time.time()
    logging.getLogger().debug(process_data_set(data))
    # Epilogue
    logging.getLogger().debug(time.time() - start)


if __name__ == "__main__":
    main()
