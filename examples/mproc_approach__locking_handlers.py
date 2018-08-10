#!/usr/bin/env python

__author__ = 'brianoneill'

__doc__ = """
A "locking handlers" version of the second approach listed in

   `Logging to a single file from multiple processes
   <https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes>`_

in the Logging Cookbook.
"""

try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['..']          # , '../..'
from prelogging import LCDict
from prelogging.six import PY2
if PY2:
    exit("%s: logging.handlers.QueueHandler doesn't exist in Python 2"
         % __file__)

import logging
import logging.handlers
from multiprocessing import Process, Queue
import random
import threading
import time
import os


def worker_config_logging():
    # DON'T attach handlers to root
    lcd = LCDict(log_path='_log/mproc_LH', root_level='DEBUG')

    lcd.add_formatter('detailed',
                      format='%(asctime)s %(name)-15s %(levelname)-8s '
                             '%(processName)-10s %(message)s',
    ).add_formatter('less-detailed',
                    format='%(name)-15s %(levelname)-8s '
                           '%(processName)-10s %(message)s')

    # lcd.add_stderr_handler('console', level='INFO',
    #                                   formatter='less-detailed')

    lcd.add_file_handler('file', filename='mplog.log',
                                 mode='w',
                                 formatter='detailed'
    ).add_file_handler('errors', level='ERROR',
                                 filename='mplog-errors.log',
                                 mode='w',
                                 formatter='detailed'
    ).attach_root_handlers(# 'console',
                           'file', 'errors')

    lcd.add_file_handler('foofile', filename='mplog-foo.log',
                                    mode='w',
                                    formatter='detailed'
    ).add_logger('foo', handlers='foofile')

    lcd.config()


def worker_process(chunksize):
    "Configuration: worker_config_logging"
    worker_config_logging()

    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
              logging.CRITICAL]
    loggers = ['foo', 'foo.bar', 'foo.bar.baz',
               'spam', 'spam.ham', 'spam.ham.eggs']
    for i in range(chunksize):
        lvl = random.choice(levels)
        logger = logging.getLogger(random.choice(loggers))
        logger.log(lvl, 'Message no. %d', i+1)
        time.sleep(random.random() / 8)


def main():
    CHUNKSIZE = 10  # 2500 -- 2m40s

    t0 = time.perf_counter()

    workers = []
    for i in range(os.cpu_count()):
        wp = Process(target=worker_process,
                     name='worker %d' % (i + 1),
                     args=(CHUNKSIZE,))
        workers.append(wp)
        wp.start()

    # At this point, the main process could do some useful work of its own...
    # Once it has done that, it can wait for the workers to terminate...

    for wp in workers:
        wp.join()

    t_elapsed = time.perf_counter() - t0
    print("\nElapsed time: %.3f" % t_elapsed)


if __name__ == '__main__':
    main()
