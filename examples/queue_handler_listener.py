#!/usr/bin/env python

__author__ = 'brianoneill'

__doc__ = """
An example that illustrates how to use a QueueListener with `lcd` so that
messages can be logged on a separate thread. In this way, handlers that block
and take long to complete (e.g. SMTP handlers, which send emails) won't make
other threads (e.g. the UI thread) stall and stutter.

For motivation, see

    `Dealing with handlers that block
    <https://docs.python.org/3/howto/logging-cookbook.html#dealing-with-handlers-that-block>`_

We've adapted the code in that section to `lcd`.

Another approach can be found in the example
``mproc_approach__queue_handler_logging_thread.py``.
"""

import logging

try:
    import lcd
except ImportError:
    import sys
    sys.path[0:0] = ['..']          # , '../..'
from lcd import LCDict

from lcd.six import PY2

if PY2:
    from Queue import Queue
else:
    from queue import Queue

def main():
    if PY2:
        import sys
        print("%s: logging.handlers.QueueHandler doesn't exist in Python 2"
              % __file__)
        return

    q = Queue(-1)  # no limit on size

    lcdx = LCDict(attach_handlers_to_root=True)
    lcdx.add_formatter(
        'fmtr', format='%(threadName)s: %(name)s: %(message)s'
    ).add_stderr_handler(
        'con', formatter='fmtr'
    ).add_queue_handler(
        'qhandler', queue=q
    ).config()

    root = logging.getLogger()

    # NOTE the following kludge for obtaining references to the QueueHandlers
    # attached to root:
    qhandlers = [handler for handler in root.handlers
                 if isinstance(handler, logging.handlers.QueueHandler)]

    listener = logging.handlers.QueueListener(q, * qhandlers)
    listener.start()
    # The log output will display the thread which generated
    # the event (the main thread) rather than the internal
    # thread which monitors the internal queue. This is what
    # you want to happen.
    root.warning('Look out!')
    listener.stop()

    # which, when run, will produce:
    # MainThread: root: Look out!


if __name__ == '__main__':
    main()

