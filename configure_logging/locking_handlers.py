# coding=utf-8

__author__ = 'brianoneill'

__doc__ = """ \
"""

import logging
from multiprocessing import Lock

__all__ = [
    'MPLock_Mixin',
    'LockingStreamHandler',
    'LockingFileHandler',
    'LockingRotatingFileHandler',
    'LockingSysLogHandler',
]

#############################################################################
# LockingStreamHandler, LockingFileHandler, LockingRotatingFileHandler,
# LockingSysLogHandler
# locking subclasses of logging package's
#       StreamHandler, FileHandler, RotatingFileHandler, SysLogHandler
#
# MPLock_Mixin -- a helper class mixed in to the Locking*Handler classes
#############################################################################

class MPLock_Mixin():
    """Mix in to a class with an instance attribute ``_mp_lock_``.
    That class should

        * initialize ``_mp_lock_``
        * call _acquire_ and _release_

    as appropriate.

    Each ``Locking*Handler`` class subclasses both this and a `logging` Handler
    class.
    """
    def _acquire_(self):
        if self._mp_lock_:
            self._mp_lock_.acquire()

    def _release_(self):
        if self._mp_lock_:
            self._mp_lock_.release()


class LockingStreamHandler(logging.StreamHandler, MPLock_Mixin):
    """
    .. _LockingStreamHandler:

    A multiprocessing-safe handler class that writes formatted logging records
    to a stream. This class doesn't close the stream, as ``sys.stdout`` or
    ``sys.stderr`` may be used.

    For more information, see the documentation for the base class
    `logging.StreamHandler <https://docs.python.org/3/library/logging.handlers.html?highlight=logging#logging.StreamHandler>`_.
    """
    def __init__(self,
                 stream=None,
                 create_lock=False,
                 **kwargs):
        """Initialize the handler.
        If stream is not specified, sys.stderr is used.
        """
        self._mp_lock_ = Lock() if create_lock else None
        super(LockingStreamHandler, self).__init__(stream=stream, **kwargs)

    # def flush(self):
    #     """Flushes the stream. Called by `logging`.
    #     """
    #     super(LockingStreamHandler, self).flush()

    def emit(self, record):
        """Emit a logging record. Called by `logging`.
        """
        self._acquire_()
        super(LockingStreamHandler, self).emit(record)      # this calls flush()
        self._release_()


class LockingFileHandler(logging.FileHandler, MPLock_Mixin):
    """
    .. _LockingFileHandler:

    A multiprocessing-safe handler class that writes
    formatted logging records to disk files.

    For more information, see the documentation for the base class
    `logging.FileHandler <https://docs.python.org/3/library/logging.handlers.html?highlight=logging#filehandler>`_.
    """
    def __init__(self, filename,
                 # mode='a', encoding=None, delay=False,
                 create_lock=False,
                 **kwargs):
        """Open the specified file and use it as the stream for logging.
        """
        self._mp_lock_ = Lock() if create_lock else None
        super(LockingFileHandler, self).__init__(
            filename,
            # mode=mode, encoding=encoding, delay=delay,
            **kwargs)

    def emit(self, record):
        """Emit a logging record. Called by `logging`.
        """
        self._acquire_()
        super(LockingFileHandler, self).emit(record)
        self._release_()


from logging import handlers

class LockingRotatingFileHandler(logging.handlers.RotatingFileHandler, MPLock_Mixin):
    """
    .. _LockingRotatingFileHandler:

    A multiprocessing-safe handler class that writes
    formatted logging records to a rotating set of disk files.

    For more information, see the documentation for the base class
    `logging.handlers.RotatingFileHandler <https://docs.python.org/3/library/logging.handlers.html?highlight=logging#rotatingfilehandler>`_.
    """
    def __init__(self, filename,
                 # mode='a', encoding=None, delay=False,
                 create_lock=False,
                 **kwargs):
        """Open the specified file and use it as the stream for logging.
        """
        self._mp_lock_ = Lock() if create_lock else None
        super(LockingRotatingFileHandler, self).__init__(
            filename,
            # mode=mode, encoding=encoding, delay=delay,
            **kwargs)

    def emit(self, record):
        """Emit a logging record. Called by `logging`.
        """
        self._acquire_()
        super(LockingRotatingFileHandler, self).emit(record)
        self._release_()
        self.close()        # . <-- Note well


# import socket
# from logging.handlers import SysLogHandler, SYSLOG_UDP_PORT
from logging.handlers import SysLogHandler

class LockingSysLogHandler(SysLogHandler, MPLock_Mixin):
    """
    .. _LockingSysLogHandler:

    A multiprocessing-safe handler class that writes
    formatted logging records to the system log.

    For more information, see the documentation for the base class
    `logging.handlers.SysLogHandler <https://docs.python.org/3/library/logging.handlers.html#sysloghandler>`_.
    """
    def __init__(self,
                 # address=('localhost', SYSLOG_UDP_PORT),
                 # facility=SysLogHandler.LOG_USER,
                 # socktype=socket.SOCK_DGRAM,
                 create_lock=False,
                 **kwargs):
        """Open the specified socket and use it as the destination for logging.
        """
        self._mp_lock_ = Lock() if create_lock else None
        super(LockingSysLogHandler, self).__init__(
                        # address=address, facility=facility, socktype=socktype,
                        **kwargs)

    def emit(self, record):
        """Emit a logging record. Called by `logging`.
        """
        self._acquire_()
        super(LockingSysLogHandler, self).emit(record)
        self._release_()
