.. _locking-handlers:

Locking Handlers
===============================

The multiprocessing-safe handler classes ``LockingStreamHandler``,
``LockingFileHandler``, ``LockingRotatingFileHandler`` and
``LockingSyslogHandler``  all use the mixin class ``MPLock_Mixin`` to
wrap a lock around calls to ``emit``. All these classes reside in
``locking_handlers.py``.

The :ref:`LCDict` class provides an interface to the locking handlers;
in the ordinary course of things it's probably unnecessary to use them directly.

.. automodule:: prelogging.locking_handlers
    :members:
