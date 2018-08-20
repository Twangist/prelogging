#!/usr/bin/env python

__author__ = 'brianoneill'

__doc__ = """
An example that illustrates how to use a QueueListener with `prelogging` so that
messages can be logged on a separate thread. In this way, handlers that block
and take long to complete (e.g. SMTP handlers, which send emails) won't make
other threads (e.g. the UI thread) stall and stutter.

For motivation, see

    `Dealing with handlers that block
    <https://docs.python.org/3/howto/logging-cookbook.html#dealing-with-handlers-that-block>`_

We've adapted the code in that section to `prelogging`.

Another approach can be found in the example
``mproc_approach__queue_handler_logging_thread.py``.
"""

import logging

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

from queue import Queue
from time import sleep


def main():

    q = Queue(-1)  # no limit on size

    LCDict(
        attach_handlers_to_root=True
    ).add_formatter(
        'fmtr', format='%(threadName)s: %(name)s: %(levelname)-8s: %(message)s'
    ).add_stderr_handler(
        'con', formatter='fmtr'
    ).add_queue_handler(
        'qhandler', queue=q
    ).config()

    root = logging.getLogger()

    # NOTE the following kludge for obtaining a reference to the QueueHandler
    # attached to root. As of Py3.7, the ``handlers`` attribute of a Logger
    # is undocumented. A more concise way to write the condition is to use
    # the ``name`` property of Handlers, also undocumented as of 3.7:
    #       if handler.name == 'qhandler'
    #
    the_qhandler = [handler for handler in root.handlers
                    if isinstance(handler, logging.handlers.QueueHandler)][0]
    listener = logging.handlers.QueueListener(q, the_qhandler)
    listener.start()
    # The log output will display the thread which generated
    # the event (the main thread) rather than the internal
    # thread which monitors the internal queue. This is what
    # you want to happen.
    root.warning('Look out!')
    sleep(1)
    root.error('Too late!')
    listener.stop()

    # which, when run, will produce:
    # MainThread: root: WARNING : Look out!
    # MainThread: root: ERROR   : Too late!


if __name__ == '__main__':
    main()
