#!/usr/bin/env python

__author__ = 'brianoneill'

__doc__ = """
An `lcd` version of the second variant in

   `Logging to a single file from multiple processes
   <https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes>`_

in the Logging Cookbook. Some small changes, some refactoring.
"""

try:
    import lcd
except ImportError:
    import sys
    sys.path[0:0] = ['..']          # , '../..'
from lcd import LoggingConfigDictEx
from lcd.six import PY2

import logging
import logging.handlers
from multiprocessing import Process, Queue

import random
import threading
import time


def worker_config_logging(q):
    lcd = LoggingConfigDictEx(attach_handlers_to_root=True, root_level='DEBUG')
    lcd.add_queue_handler('qhandler', queue=q)
    lcd.config()


def worker_process(q):
    "Configuration: worker_config_logging"
    worker_config_logging(q)

    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
              logging.CRITICAL]
    loggers = ['foo', 'foo.bar', 'foo.bar.baz',
               'spam', 'spam.ham', 'spam.ham.eggs']
    for i in range(100):
        lvl = random.choice(levels)
        logger = logging.getLogger(random.choice(loggers))
        logger.log(lvl, 'Message no. %d', i+1)
        time.sleep(random.random()/8)


def logging_thread(q):
    "Configuration: main_process_config_logging"
    while True:
        record = q.get()        # TODO: does `q` itself need a lock? accessing it should block?
        if record is None:
            break
        logger = logging.getLogger(record.name)
        logger.handle(record)


def main_process_config_logging():
    # DON'T attach handlers to root
    lcd = LoggingConfigDictEx(log_path='_log/mproc_QHLT', root_level='DEBUG')

    lcd.add_formatter('detailed',
                      format='%(asctime)s %(name)-15s %(levelname)-8s '
                             '%(processName)-10s %(message)s',
    ).add_formatter('less-detailed',
                    format='%(name)-15s %(levelname)-8s '
                           '%(processName)-10s %(message)s')

    lcd.add_stderr_handler('console', level='INFO',
                                              formatter='less-detailed'
    ).add_file_handler('file', filename='mplog.log',
                               formatter='detailed'
    ).add_file_handler('errors', level='ERROR',
                                 filename='mplog-errors.log',
                                 formatter='detailed'
    ).attach_root_handlers('console', 'file', 'errors')

    lcd.add_file_handler('foofile', filename='mplog-foo.log',
                                    formatter='detailed'
    ).add_logger('foo', handlers='foofile')

    lcd.config()


def main():
    if PY2:
        import sys
        print("%s: logging.handlers.QueueHandler doesn't exist in Python 2"
              % __file__)
        return

    main_process_config_logging()

    q = Queue()
    workers = []
    for i in range(5):
        wp = Process(target=worker_process,
                     name='worker %d' % (i + 1),
                     args=(q,))
        workers.append(wp)
        wp.start()

    the_log_thread = threading.Thread(target=logging_thread, args=(q,))
    the_log_thread.start()

    # At this point, the main process could do some useful work of its own...

    # TODO: Do something such that you'd notice it stall and stutter
    #  |    if the logging handlers were running in the same process and thread

    # Once it has done that, it can wait for the workers to terminate...

    for wp in workers:
        wp.join()

    # Now tell the logging thread to finish up too
    q.put(None)
    the_log_thread.join()

if __name__ == '__main__':
    main()
