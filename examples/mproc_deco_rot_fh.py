#!/usr/bin/env python

__author__ = 'brianoneill'
__version__ = '0.2'

try:
    from deco import *
except ImportError:
    exit("`mproc_deco_rot_fh.py` requires the `deco` package -- "
         "https://github.com/alex-sherman/deco")

import time
import random
from collections import defaultdict
import logging

try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['..', '../..']
from prelogging import LCDict

from examples._get_locking_pref import get_locking_pref

LOGFILENAME = 'rot_fh.log'

#############################################################################

@concurrent(processes=3)     # add this for the concurrent function
def process_lat_lon(lat, lon, data):
    time.sleep(0.1)

    logging.getLogger().info("processing lat, lon = %d, %d"
                             "\n\t              %d, %d"
                             % (lat, lon, lat, lon)
                             # % (lat, lon)
                             )
    return data[lat + lon]


@synchronized   # add this for the function that calls the concurrent function
def process_data_set(data):
    results = defaultdict(dict)
    for lat in range(6):
        for lon in range(6):
            logging.getLogger().info("lat, lon = %d, %d" % (lat, lon))

            results[lat][lon] = process_lat_lon(lat, lon, data)

    return dict(results)


import os

def config_logging(use_locking):
    # NOTE: log_path dir should already exist
    log_path = os.path.join('_log/mproc_deco_rot_fh', 'LOCKING' if use_locking else 'NOLOCKING')
    lcd = LCDict(log_path=log_path,
                 root_level='DEBUG',
                 attach_handlers_to_root=True,
                 locking=use_locking)
    # Set up console handler to show process name, time, handler name
    lcd.add_stderr_handler(
        'console', formatter='process_level_msg', level='INFO'
    )
    # Add main file handler, which will write to log_path + '/' + logfilename
    lcd.add_rotating_file_handler(
        'rot_fh',
        filename=LOGFILENAME,
        # formatter='process_time_level_msg',
        max_bytes=1024,
        backup_count=10,
        # mode='w',
    )
    lcd.config()


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
    main()
