`LCDict` Features and Usage
===============================================

``LCDict`` subclasses ``LCDictBasic`` to contribute additional
conveniences:

* :ref:`formatter presets <LCDict-using-formatter-presets>`;
* various ``add_*_handler`` methods for configuring handlers of several
  `logging` handler classes — see the :ref:`table below <LCDict-handler-classes-encapsulated>`;
* optional automatic attaching of handlers to the root logger
  as they're added;
* easy use of the "locking" (multiprocessing-safe) handler classes
  that `prelogging` provides;
* simplified filter creation.

The class is fully documented in :ref:`LCDict`. This chapter discusses
its added features, along with other topics common to both ``LCDict*`` classes
which provide the context for those features.

.. _using-formatters:

Using formatters
-------------------------------------------------------

We've already seen examples of adding new formatters using ``add_formatter``.
(See the documentation of that method in :ref:`LCDict` for details of its
parameters and their possible values.)

As our :ref:`first example <config-use-case-lcdict>` indicated,
often it's not necessary to specify formatters from scratch,
because ``LCDict`` provides about a dozen formatter "presets" —
predefined formatter specifications that are often needed.
The following table exhibits all of them:

.. _LCDict-using-formatter-presets:
.. _preset-formatters:

.. index:: preset formatters (LCDict), formatter presets (LCDict)

+--------------------------------------+-----------------------------------------------------------------------------------+
|| Formatter name                      || Format string                                                                    |
+======================================+===================================================================================+
|| ``'msg'``                           || ``'%(message)s'``                                                                |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'level_msg'``                     || ``'%(levelname)-8s: %(message)s'``                                               |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'process_msg'``                   || ``'%(processName)-10s: %(message)s'``                                            |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'logger_process_msg'``            || ``'%(name)-20s: %(processName)-10s: %(message)s'``                               |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'logger_level_msg'``              || ``'%(name)-20s: %(levelname)-8s: %(message)s'``                                  |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'logger_msg'``                    || ``'%(name)-20s: %(message)s'``                                                   |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'process_level_msg'``             || ``'%(processName)-10s: %(levelname)-8s: %(message)s'``                           |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'process_time_level_msg'``        || ``'%(processName)-10s: %(asctime)s: %(levelname)-8s: %(message)s'``              |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'process_logger_level_msg'``      || ``'%(processName)-10s: %(name)-20s: %(levelname)-8s: %(message)s'``              |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'process_time_logger_level_msg'`` || ``'%(processName)-10s: %(asctime)s: %(name)-20s: %(levelname)-8s: %(message)s'`` |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'time_logger_level_msg'``         || ``'%(asctime)s: %(name)-20s: %(levelname)-8s: %(message)s'``                     |
+--------------------------------------+-----------------------------------------------------------------------------------+

Creating new formatter presets
++++++++++++++++++++++++++++++++

.. todo:: Adding formatter presets (todo: this too)

    You can do this. <SAY briefly why you might want to.> See
    :ref:`adding-new-formatter-presets` for details.

    mainly useful for "distributed" configuration, where multiple
    modules or packages all build one logging config dict.

    The top-level, "driver" can create formatter presets for
    the modules/packages to use.

    Reference/link ``LCDictBuilderABC``,
    mini-framework for just such a situation.

.. _using-create_formatter_preset-with-LCDictBuilderABC:

.. todo:: Does this go in the ``LCDictBuilderABC`` section? Probably.
    And give a link here to this discussion moved to there.

.. topic:: How to use ``create_formatter_preset`` with ``LCDictBuilderABC``

    Define a subclass ``LCDictBuilderABC`` — say, ``LCDictBuilder``.
    Every other module or package
    that modifies the common ``LCDict`` being built should subclass the
    ``LCDictBuilder`` class. All these class will implement ``add_to_lcdict(lcd)``
    and modify ``lcd`` there.

    ``add_to_lcdict(lcd)`` will be called on every ``LCDictBuilderABC`` subclass
    that implements it, **in breadth-first order** with respect to inheritance.
    Thus, ``LCDictBuilder.add_to_lcdict(lcd)`` will be called **first**;
    ``subcls.add_to_lcdict(lcd)`` will be called subsequently for each
    subclass ``subcls`` of ``LCDictBuilder``.

    In ``LCDictBuilder``, implement ``add_to_lcdict`` and create new formatter
    presets there; use those presets in (``add_to_lcdict`` implementations in)
    subclasses of ``LCDictBuilder``.

    **Note** Be sure to import all these ``LCDictBuilderABC`` subclasses
    before calling ``LCDictBuilder.build_lcdict``.


------------------------------------------------------

.. _adding-handlers:

Adding handlers
--------------------

The `logging` package defines more than a dozen handler classes — subclasses of
``logging.Handler`` — in the modules ``logging`` and ``logging.handlers``.
``logging`` defines the basic stream, file and null handler classes, for which
``LCDictBasic`` supplies  ``add_*_handler`` methods. ``logging.handlers`` defines
more specialized handler classes, for about half of which (presently) ``LCDict``
provides corresponding ``add_*_handler`` methods.

.. _add-console-handler:

Adding a console handler
++++++++++++++++++++++++++
<<<<< TODO >>>>>

.. _add-file-handler:

Adding a file handler
++++++++++++++++++++++++++
<<<<< TODO >>>>>

.. _LCDict-handler-classes-encapsulated:

.. index:: `'logging` handler classes encapsulated

Handler classes that LCDict configures
++++++++++++++++++++++++++++++++++++++++++

LCDict provides methods for configuring these `logging` handler classes,
all defined in the ``logging.handlers`` module, with optional "locking" support
in most cases:

  +--------------------------------+---------------------------+-----------+
  || method                        || creates                  || optional |
  ||                               ||                          || locking? |
  +================================+===========================+===========+
  || ``add_stderr_handler``        || stderr ``StreamHandler`` ||   yes    |
  || ``add_stdout_handler``        || stdout ``StreamHandler`` ||   yes    |
  || ``add_file_handler``          || ``FileHandler``          ||   yes    |
  || ``add_rotating_file_handler`` || ``RotatingFileHandler``  ||   yes    |
  || ``add_syslog_handler``        || ``SyslogHandler``        ||   yes    |
  || ``add_email_handler``         || ``SMTPHandler``          ||          |
  || ``add_queue_handler``         || ``QueueHandler``         ||          |
  || ``add_null_handler``          || ``NullHandler``          ||          |
  +--------------------------------+---------------------------+-----------+

.. _add-other-handler:

Adding other kinds of handlers
+++++++++++++++++++++++++++++++++

LCDict encapsulates :ref: about half of the classes defined in ``logging.handlers``,
as shown in :ref:`this table<LCDict-handler-classes-encapsulated>`. The
following `logging` handler classes presently have no corresponding
``add_*_handler`` methods:

* logging.handlers.WatchedFileHandler
* logging.handlers.TimedRotatingFileHandler
* logging.handlers.SocketHandler
* logging.handlers.DatagramHandler
* logging.handlers.NTEventLogHandler
* logging.handlers.MemoryHandler
* logging.handlers.HTTPHandler

Future versions of `prelogging` may supply methods for these handler classes.
In any case, all can be configured using `prelogging` currently. It is
straightforward to write ``add_*_handler`` methods for any or all of these,
on the model of the existing methods, which call ``add_handler`` with the
appropriate handler class as value of the ``class_`` keyword, and passing any
other class-specific key/value pairs as keyword arguments.


