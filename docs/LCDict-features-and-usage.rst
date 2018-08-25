.. include:: _global.rst

.. _lcdict-features:

`LCDict` Features and Usage
===============================================

``LCDict`` subclasses ``LCDictBasic`` to contribute additional
conveniences. The class is fully documented in :ref:`LCDict`.
In this chapter we describe the features it adds:

* :ref:`using formatter presets <formatter_presets_in_LCDict>`
* :ref:`add_*_handler methods for several classes in logging.handlers <supported-handlers>`
* :ref:`optional automatic attaching of handlers to the root logger as they're added <auto-attach-handlers-to-root>`
* :ref:`easy multiprocessing-safe logging <easy-mp-safe-logging>`
* :ref:`simplified creation and use of filters <filters>`.

.. _formatter_presets_in_LCDict:

Using formatter presets
-------------------------------------------------------

We've already seen simple examples of adding new formatters using
``add_formatter``. The documentation of that method in :ref:`LCDictBasic`
details its parameters and their possible values.

As our :ref:`first example <config-use-case-lcdict>` indicated,
often it's not necessary to specify formatters from scratch,
because `prelogging` provides an extensible, modifiable collection of *formatter
presets* — predefined formatter specifications which cover many needs.
You can use the name of any of these presets as the ``formatter`` argument
to ``add_*_handler`` methods and to ``set_handler_formatter``. `prelogging` ships
with about a dozen of them, shown in :ref:`this table <preset-formatters-table>`.

.. index:: formatter presets (added to an LCDict only when used)

.. _LCDict-using-formatter-presets:

Formatter presets are added to an ``LCDict`` "just in time", when they're used::

    >>> lcd = LCDict()
    >>> # The underlying dict of a "blank" LCDict
    >>> #   is the same as that of a blank LCDictBasic --
    >>> #   lcd.formatters is empty:
    >>> lcd.dump()
    {'disable_existing_loggers': False,
     'filters': {},
     'formatters': {},
     'handlers': {},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': [], 'level': 'WARNING'},
     'version': 1}

    >>> # Using the 'level_msg' preset adds it to lcd.formatters:
    >>> _ = lcd.add_stderr_handler('console', formatter='level_msg')
    >>> lcd.dump()
    {'disable_existing_loggers': False,
     'filters': {},
     'formatters': {'level_msg': {'class': 'logging.Formatter',
                                  'format': '%(levelname)-8s: %(message)s'}},
     'handlers': {'console': {'class': 'logging.StreamHandler',
                              'formatter': 'level_msg',
                              'level': 'NOTSET',
                              'stream': 'ext://sys.stderr'}},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': [], 'level': 'WARNING'},
     'version': 1}

Only ``'level_msg'`` has been added to ``lcd.formatters``.

Of course, the dozen or so formatter presets that `prelogging` contains,
aren't a comprehensive collection, and probably won't meet everyone's needs
or suit everyone's tastes. Therefore `prelogging` provides two functions that
let you add your own presets, and/or modify existing ones:

    * ``update_formatter_presets_from_file(filename)``, and
    * ``update_formatter_presets(multiline_str)``.

These functions, and the formats of their arguments, are described in the chapter
:ref:`Formatter Presets <preset-formatters-chapter>` following this one.

------------------------------------------------------

.. _supported-handlers:

Handler classes encapsulated by ``LCDict``
-----------------------------------------------------

`logging` defines more than a dozen handler classes — subclasses of
``logging.Handler`` — in the modules ``logging`` and ``logging.handlers``.
The package defines the basic stream, file and null handler classes,
for which ``LCDictBasic`` supplies  ``add_*_handler`` methods. Its ``handlers``
module defines more specialized handler classes, for about half of which (presently)
``LCDict`` provides corresponding ``add_*_handler`` methods.

.. index:: logging handler classes encapsulated

.. _LCDict-handler-classes-encapsulated:

Handler classes that LCDict configures
++++++++++++++++++++++++++++++++++++++++++

LCDict provides methods for configuring these `logging` handler classes, with
optional "locking" support in most cases:

  +--------------------------------+---------------------------+-----------+
  || method                        || creates                  || optional |
  ||                               ||                          || locking? |
  +================================+===========================+===========+
  || ``add_stream_handler``        || ``StreamHandler``        ||   yes    |
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

The following `logging` handler classes presently have no corresponding
``add_*_handler`` methods:

* logging.handlers.WatchedFileHandler
* logging.handlers.TimedRotatingFileHandler
* logging.handlers.SocketHandler
* logging.handlers.DatagramHandler
* logging.handlers.MemoryHandler
* logging.handlers.NTEventLogHandler
* logging.handlers.HTTPHandler

Future versions of `prelogging` may supply methods for at least some of these.
In any case, all can be configured using `prelogging`. It's straightforward to
write ``add_*_handler`` methods for any or all of these classes, on the model of
the existing methods: call ``add_handler`` with the appropriate handler class as
value of the ``class_`` keyword, and pass any other class-specific key/value
pairs as keyword arguments.

------------------------------------------------------

.. _auto-attach-handlers-to-root:

Automatically attaching handlers to the root logger
--------------------------------------------------------

Because handlers are so commonly attached to the root logger,
``LCDict`` makes it easy to do that. Two parameters and their defaults
govern this:

* The initializer method ``LCDict.__init__`` has a boolean parameter
  ``attach_handlers_to_root`` [default: ``False``].

  Each instance saves the value passed to its constructor, and exposes it as the
  read-only property ``attach_handlers_to_root``.
  When ``attach_handlers_to_root`` is true, by default the
  handler-adding methods of this class automatically attach handlers to
  the root logger after adding them to the ``handlers`` subdictionary.
  |br10th|
  |br10th|
* All ``add_*_handler`` methods **called on an** ``LCDict``, as well as
  the ``clone_handler`` method, have an ``attach_to_root`` parameter
  [type: ``bool`` or ``None``; default: ``None``].
  The ``attach_to_root`` parameter
  allows overriding of the value ``attach_handlers_to_root`` passed to
  the constructor.

  The default value of ``attach_to_root``
  is ``None``, which is interpreted to mean: use the value of
  ``attach_handlers_to_root`` passed to the constructor. If ``attach_to_root``
  has any value other than ``None``,
  the handler will be attached *iff* ``attach_to_root`` is true/truthy.

Thus, if ``lcd`` is an ``LCDict`` created with ``attach_handlers_to_root=True``,

    ``lcd = LCDict(attach_handlers_to_root=True, ...)``

you can still add a handler to ``lcd`` without attaching it to the root::

    lcd.add_stdout_handler('stdout', attach_to_root=False, ...)

Similarly, if lcd`` is created with ``attach_handlers_to_root=False`` (the default),

    ``lcd = LCDict(...)``

you can attach a handler to the root as soon as you add it to ``lcd``::

    lcd.add_file_handler('fh', filename='myfile.log', attach_to_root=True, ...)

without having to subsequently call ``lcd.attach_root_handlers('fh', ...)``.


------------------------------------------------------

.. _easy-mp-safe-logging:

Easy multiprocessing-safe logging
--------------------------------------------------------------------------

As we've mentioned, most recently in the this chapter's earlier section
:ref:`LCDict-handler-classes-encapsulated`,
`prelogging` provides multiprocessing-safe ("locking") versions of the essential
handler classes that write to the console, streams, files, rotating files, and
syslog. These subclasses of handler classes defined by
`logging` are documented in :ref:`locking-handlers`. The following ``LCDict``
methods:

  | ``add_stream_handler``
  | ``add_stderr_handler``
  | ``add_stdout_handler``
  | ``add_file_handler``
  | ``add_rotating_file_handler``
  | ``add_syslog_handler``

can create either a standard, `logging` handler or a locking version thereof.
Two keyword parameters and their defaults govern which type of handler
will be created:

* The initializer method ``LCDict.__init__`` has a boolean parameter
  ``locking`` [default: ``False``].

  Each ``LCDict`` instance saves the value passed to its constructor,
  and exposes it as the read-only property ``locking``.
  When ``locking`` is true, by default the ``add_*_handler`` methods listed above
  will create locking handlers.
  |br10th|
  |br10th|
* The ``add_*_handler`` methods listed above have a ``locking`` parameter
  [type: ``bool`` or ``None``; default: ``None``], which
  allows overriding of the value ``locking`` passed to the constructor.

  The default value of the ``add_*_handler`` parameter ``locking``
  is ``None``, which is interpreted to mean: use the value of
  ``locking`` passed to the constructor. If the ``add_*_handler`` parameter
  ``locking`` has any value other than ``None``,
  a locking handler will be created *iff* the parameter's value is true/truthy.

------------------------------------------------------

.. _easy-filter-creation:
.. _filters:

Simplified creation and use of filters
------------------------------------------

Filters allow finer control than mere loglevel comparison over which messages
actually get logged.

There are two kinds of filters: class filters and callable filters.
``LCDict`` provides a pair of convenience methods, ``add_class_filter`` and
``add_callable_filter``, which are easier to use than the lower-level
``LCDictBasic`` method ``add_filter``.

In Python 2, the `logging` module imposes a fussy requirement on callables
that can be used as filters, which the Python 3 implementation of `logging`
removes. The ``add_callable_filter`` method provides a single interface for
adding callable filters that works in both Python versions.

.. _filter-setup:

Defining filters
++++++++++++++++++++++++++++++++

Here are a couple of examples of filters, both of which suppress
certain kinds of messages. Each has the side effect of incrementing
a distinct global variable.

Class filters
~~~~~~~~~~~~~~~~~~~~~~

Classic filters are instances of any class that implement a ``filter`` method
with the following signature::

        filter(self, record: logging.LogRecord) -> int

where ``int`` is treated like ``bool`` — nonzero means true (log the record),
zero means false (don't). These include subclasses of ``logging.Filter``, but
a filter class doesn't have to inherit from that `logging` class.

Class filter example
^^^^^^^^^^^^^^^^^^^^^^^^
.. code::

    _info_count = 0     # incremented by the following class filter

    class CountInfoSquelchOdd():
        def filter(self, record):
            """Suppress odd-numbered messages (records) whose level == INFO,
            where the "first" message is the 0-th hence is even-numbered.

            :param self: unused
            :param record: logging.LogRecord
            :return: int -- true (nonzero) ==> let record through,
                            false (0) ==> squelch
            """
            global _info_count
            if record.levelno == logging.INFO:
                _info_count += 1
                return _info_count % 2
            else:
                return True

Callable filters
~~~~~~~~~~~~~~~~~~~~~~
A filter can also be a callable, of signature ``logging.LogRecord -> int``.
(In fact, `prelogging` lets you use callables of signature
``(logging.LogRecord, **kwargs) -> int``; see the section below on
:ref:`providing extra, static data to callable filters <providing-extra-static-data-to-a-filter-callable>`
for discussion and an example.)

Callable filter example
^^^^^^^^^^^^^^^^^^^^^^^^
.. code::

    _debug_count = 0        # incremented by the following callable filter

    def count_debug_allow_2(record):
        """
        Allow at most 2 messages with loglevel ``DEBUG``.

        :param record: ``logging.LogRecord``
        :return: ``bool`` -- True ==> let record through, False ==> squelch
        """
        global _debug_count
        if record.levelno == logging.DEBUG:
            _debug_count += 1
            return _debug_count <= 2
        else:
            return True


.. _tr-filters-logger:

Filters on the root logger
+++++++++++++++++++++++++++++

Let's configure the root logger to use both filters shown above::

    lcd = LCDict(
        attach_handlers_to_root=True,
        root_level='DEBUG')

    lcd.add_stdout_handler(
        'console',
        level='DEBUG',
        formatter='level_msg')

    lcd.add_callable_filter('count_d', count_debug_allow_2)
    lcd.add_class_filter('count_i', CountInfoSquelchOdd)

    lcd.attach_root_filters('count_d', 'count_i')

    lcd.config()

Now use the root logger::

    import logging
    root = logging.getLogger()

    for i in range(5):
        root.debug(str(i))
        root.info(str(i))

    print("_debug_count:", _debug_count)
    print("_info_count:", _info_count)

This passage writes the following to ``stdout``::

    DEBUG   : 0
    INFO    : 0
    DEBUG   : 1
    INFO    : 2
    INFO    : 4
    _debug_count: 5
    _info_count: 5

.. note::
    This example **is** the test ``test_add_xxx_filter.py``, with little
    modification.


Filters on a non-root logger
+++++++++++++++++++++++++++++

Attaching the example filters to a non-root logger ``'mylogger'`` requires just
one change: instead of using ``attach_root_filters`` to
attach the filters to the root logger, now we have to attach them to an
arbitrary logger. This can be accomplished in either of two ways:

* Attach the filters when calling ``add_logger`` for ``'mylogger'``, using the
  ``filters`` keyword parameter::

    lcd.add_logger('mylogger',
                      filters=['count_d', 'count_i'],
                      ...
                     )

  The value of the ``filters`` parameter can be either the name of a single
  filter (a ``str``) or a sequence (list, tuple, etc.) of names of filters.
  |br10th|
  |br10th|
* Add the logger with ``add_logger``, without using the ``filters`` parameter::

    lcd.add_logger('mylogger', ... )

  and then attach filters to it with ``attach_logger_filters``::

    lcd.attach_logger_filters('mylogger',
                              'count_d', 'count_i')

.. _tr-filters-handler:

Filters on a handler
+++++++++++++++++++++++++++++

There are two ways to attach filters to a handler:

* Attach the filters in the same method call that adds the handler.
  Every ``add_*_handler`` method takes a ``filters`` keyword parameter —
  all those methods funnel through ``LCDictBasic.add_handler``. As with the
  ``add_logger`` method, the value of the ``filters`` parameter can be either
  the name of a single filter (a ``str``) or a sequence (list, tuple, etc.) of
  names of filters.

  For example, each of the following method calls adds a handler with
  only the ``'count_d'`` filter attached::

    lcd.add_stderr_handler('con-err',
                           filters='count_d'
    ).add_file_handler('fh',
                       filename='some-logfile.log',
                       filters=['count_d'])

  For another example, the following statement adds a rotating file handler with
  both the ``'count_i'`` and ``'count_d'`` filters attached::

    lcd.add_rotating_file_handler('rfh',
                                  filename='some-rotating-logfile.log',
                                  max_bytes=1024,
                                  backup_count=5,
                                  filters=['count_i', 'count_d'])

* Add the handler using any ``add_*_handler`` method, then use
  ``add_handler_filters`` to attach filters to the handler. For example::

    lcd.add_file_handler('myhandler',
                         filename='mylogfile.log'
    ).attach_handler_filters('myhandler',
                             'count_d', 'count_i')


In :ref:`a later chapter <providing-extra-static-data-to-a-filter>` we'll
discuss providing extra data to filters, in addition to the ``LogRecord``\s
they're called with.
