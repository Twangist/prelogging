README for prelogging |version|
=================================

.. include:: docs/_global.rst


.. todo:: README.rst for `prelogging`

.. todo:: link to full docs on readthedocs

What `prelogging` is and does
------------------------------------------------

Installation
------------------------------------------------

Logging, `logging`, and Logging Configuration
------------------------------------------------

Multiprocessing-Safe logging, two ways
-----------------------------------------

* using "locking handlers", simple subclasses of `logging` handlers
  which `prelogging` provides natively << TODO -- more about this >>
* using a QueueHandler and a logging thread,
    - as explained in the docs
    - as shown in an example, ``mproc_approach__queue_handler_logging_thread.py``
    - as depicted in the following diagram

.. figure:: docs/mproc_queue_paradigm.png

    Multiprocess logging with a queue and a logging thread

-------------------------------------------------------------------------------

.. stuff to include:


.. <<<<<<<<<<<<<<<<<<<<<<<<<< TWO GOOD DIAGRAMS >>>>>>>>>>>>>>>>>>>>>>>>>>:

.. _logging-config-classes:

.. figure:: docs/logging_classes_v2.png

    The objects of `logging` configuration

    +----------------------------+-----------------------+
    | Symbol                     | Meaning               |
    +============================+=======================+
    | .. image:: docs/arrowO.png | has zero or more      |
    +----------------------------+-----------------------+
    | m: 0/1                     | many-to-(zero-or-one) |
    +----------------------------+-----------------------+
    | m: n                       | many-to-many          |
    +----------------------------+-----------------------+


In words:

    * a ``Logger`` can have one or more ``Handler``\s, and a ``Handler``
      can be used by multiple ``Logger``\s;
    * a ``Handler`` has at most one ``Formatter``, but a ``Formatter``
      can be shared by multiple ``Handler``\s;
    * ``Handler``\s and ``Logger``\s can each have zero or more ``Filter``\s;
      a ``Filter`` can be used by multiple ``Handler``\s and/or ``Logger``\s.


What these objects do
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A ``Formatter`` is basically just a format string that uses keywords
defined by the `logging` module — for example, ``'%(message)s'`` and
``'%(name)-20s: %(levelname)-8s: %(message)s'``.

A ``Handler`` formats and writes formatted logged messages to a particular
destination — a stream (e.g. ``sys.stderr``, ``sys.stdout``, or an in-memory
stream such as an ``io.StringIO()``), a file, a rotating set of files, a socket,
etc. A handler without a formatter behaves as if it had a ``'%(message)s'``
formatter.

A ``Logger`` sends logged messages to its associated handlers. Various
criteria filter out which messages are actually written, notably loglevel
thresholding as described above.

``Filter``\s provide still more fine-grained control over which messages are
written.


-------------------------------------------------------------------------------

Class diagram
----------------


.. _prelogging-all-classes:

.. figure:: docs/prelogging_classes-v4d.png
    :figwidth: 100%

    |br| **prelogging** classes — inheritance, and who uses whom

    +----------------------------+-----------------------+
    | Symbol                     | Meaning               |
    +============================+=======================+
    | .. image:: docs/arrsup.png | is a superclass of    |
    +----------------------------+-----------------------+
    | .. image:: docs/arruse.png | uses (instantiates)   |
    +----------------------------+-----------------------+

-------------------------------------------------------------------------------
