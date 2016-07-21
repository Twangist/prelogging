# coding=utf-8

__author__ = 'brianoneill'

__doc__ = """ \
This module contains multiprocessing-safe handler classes for use with `logging`.
The ``LoggingConfigDictEx`` class and its methods provide an interface to them —
in the ordinary course of things it's probably unnecessary to use them directly.

-----

"""

import logging
from multiprocessing import Lock

__all__ = [
    # 'MPLock_Mixin',
    'LockingStreamHandler',
    'LockingFileHandler',
    'LockingRotatingFileHandler',
]

#############################################################################
# LockingStreamHandler, LockingFileHandler, LockingRotatingFileHandler
# Locking subclasses of logging module's
#       StreamHandler, FileHandler, RotatingFileHandler
#############################################################################

class MPLock_Mixin():
    """Mix in to a class with an instance attribute ``_mp_lock_``.

    Each ``Locking*Handler`` class subclasses both this and a Handler class of the `logging` module.
    """
    def _acquire_(self):
        if self._mp_lock_:
            self._mp_lock_.acquire()

    def _release_(self):
        if self._mp_lock_:
            self._mp_lock_.release()


class LockingStreamHandler(logging.StreamHandler, MPLock_Mixin):
    """
    A multiprocessing-safe handler class that writes formatted logging records
    to a stream. This class doesn't close the stream, as ``sys.stdout`` or
    ``sys.stderr`` may be used.

    For more information, see the documentation for the base class `logging.StreamHandler <https://docs.python.org/3/library/logging.handlers.html?highlight=logging#logging.StreamHandler>`_.
    """
    def __init__(self, create_lock=False, stream=None):
        """Initialize the handler.
        If stream is not specified, sys.stderr is used.
        """
        self._mp_lock_ = Lock() if create_lock else None
        super(LockingStreamHandler, self).__init__(stream=stream)

    def flush(self):
        """Flushes the stream. Called by `logging`.
        """
        super(LockingStreamHandler, self).flush()

    def emit(self, record):
        """Emit a logging record. Called by `logging`.
        """
        self._acquire_()
        super(LockingStreamHandler, self).emit(record)        # this calls flush()
        self._release_()


class LockingFileHandler(logging.FileHandler, MPLock_Mixin):
    """A multiprocessing-safe handler class that writes
    formatted logging records to disk files.

    For more information, see the documentation for the base class `logging.FileHandler <https://docs.python.org/3/library/logging.handlers.html?highlight=logging#filehandler>`_.
    """
    def __init__(self, filename, create_lock=False, mode='a', encoding=None, delay=False):
        """Open the specified file and use it as the stream for logging.
        """
        self._mp_lock_ = Lock() if create_lock else None
        super(LockingFileHandler, self).__init__(
            filename, mode=mode, encoding=encoding, delay=delay)

    def emit(self, record):
        """Emit a logging record. Called by `logging`.
        """
        self._acquire_()
        super(LockingFileHandler, self).emit(record)
        self._release_()


from logging import handlers

class LockingRotatingFileHandler(logging.handlers.RotatingFileHandler, MPLock_Mixin):
    """A multiprocessing-safe handler class that writes
    formatted logging records to a rotating set of disk files.

    For more information, see the documentation for the base class `logging.RotatingFileHandler <https://docs.python.org/3/library/logging.handlers.html?highlight=logging#rotatingfilehandler>`_.
    """
    def __init__(self, filename, create_lock=False, mode='a', encoding=None, delay=False, **kwargs):
        """Open the specified file and use it as the stream for logging.
        """
        self._mp_lock_ = Lock() if create_lock else None
        super(LockingRotatingFileHandler, self).__init__(
            filename, mode=mode, encoding=encoding, delay=delay, **kwargs)

    def emit(self, record):
        """Emit a logging record. Called by `logging`.
        """
        self._acquire_()
        super(LockingRotatingFileHandler, self).emit(record)
        self._release_()
        self.close()        # . <-- Note well
