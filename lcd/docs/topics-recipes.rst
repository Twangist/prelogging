Topics and Recipes
====================

.. todo::
    Blah examples/topics blah

--------------------------------------------------

Basic usage of ``LoggingConfigDict``
-------------------------------------------------------


.. todo::
    intro blather, basic usage of ``LoggingConfigDict``

As shown in the Introduction's :ref:`class inheritance diagram <lcd-all-classes>`,
objects of this class *are* dicts.

The methods of this class —``add_formatter``, ``add_filter``,
``add_handler``, ``add_logger``, and so on — operate on the underlying dictionary.
That dict is significantly nested, and keys often appear among the data, as
back references to things "already defined".

Although dicts are unordered, when configuring logging there's a precedence ordering
for specifying objects:

    1. Create a ``LoggingConfigDict``, optionally specifying the level of the root handler

    2. Add formatter specifications with ``add_formatter()``

    3. Add any filter specifications with ``add_filter()`` (or interchange Steps 2. and 3.)

    4. Add handler specifications with ``add_handler()`` and/or ``add_file_handler()``

       In steps 2. – 4., you give each thing specified a name, by which you refer to it
       in subsequent steps when associating the thing with other, higher-level things.

    5. If desired, configure the root logger using ``add_root_handlers()``, ``add_root_filters()``
       and ``set_root_level()``.

       You refer by name to handlers and filters already specified in the previous steps.

    6. Add logger specifications, if any, with ``add_logger()``. Specify the handlers
       and filters of a logger with the ``handlers`` and ``filters`` keyword parameters.


The (leaf) values in logging config dicts are almost all strings. The exceptions are
``bool`` values and actual streams allowed as the value of ``'stream'`` in
in a handler subdict (e.g. ``stream=sys.stdout``). This package uses ``bool``
values, but not actual streams, preferring the text equivalents accepted
by the `logging` module's ``configDict()`` method:

    instead of ``stream=sys.stdout``, we use ``stream='ext://sys.stdout'``.

The reason: the ``clone_handler()`` method of the subclass ``LoggingConfigDictEx``
uses ``deepcopy()``, and streams can't be deepcopied. We recommend that you not use
actual streams, but rather the text equivalents, as shown in the example just given.



A single ``LoggingConfigDict`` can be passed around to different "areas" of a program,
each contributing specifications of its desired formatters, filters, handlers and
loggers.

.. note::
    In this class as well as in :ref:`LoggingConfigDictEx`, `level` always means the
    ``str`` name of the level, e.g. ``'DEBUG'``, not the numeric value ``logging.DEBUG``.

Once a ``LoggingConfigDict`` has been populated, it can be used to configure
logging by calling its ``config()`` method, which is basically just shorthand
for a call to ``logging.config.dictConfig()``.

--------------------------------------------------

Basic usage of ``LoggingConfigDictEx``
---------------------------------------------------------

.. todo::
    intro blather, basic usage of ``LoggingConfigDictEx``

EXAMPLE
+++++++

Start with a ``LoggingConfigDictEx`` that uses standard (non-locking) stream
and file handlers. Put logfiles in the ``_log/`` subdirectory of the current
directory. Use root loglevel ``'DEBUG'``. ::

    from lcd import LoggingConfigDictEx

Aside from the usage above, hereinafter in this example we use ``lcd``
as a variable for a (logging config) ``dict``::

    lcd = LoggingConfigDictEx(log_path='_log/',
                              root_level='DEBUG',
                              add_handlers_to_root=True)

Specify two loggers, each with its own file handler with loglevel ``'DEBUG'``::

    # Set up root logger, which will write to stderr and to a file.
    # console logger uses default log level 'WARNING',
    # file handler uses default level 'DEBUG':
    lcd.add_stderr_console_handler('console')
    lcd.add_file_handler('app_fh', filename='app.log')

    ## Instead of using "add_handlers_to_root=True" in the constructor,
    ##  we could omit that and now use:
    # lcd.add_root_handlers('console, 'app_fh')

    # Add an 'extra' logger which writes to a different file:
    lcd.add_file_handler('extra_fh', filename='app_extra.log')
    lcd.add_logger('extra', ['extra_fh'], level='DEBUG')

Prior to calling ``lcd.config()``, pass lcd to other "areas" of your program
to let them specify their loggers & such, something like::

    # add to lcd:
    module_class_or_package_name.init_logging(lcd)

Call config so create actual objects of types — logging.Formatter,
logging.Logger, etc. Do this once and once only::

    # Configure logging using these settings:
    lcd.config()

``lcd`` (the dict object) is actually no longer needed (we don't do 'incremental' config).

To use the loggers, access them by name::

    # This writes "Hi there" to file `./_log/app_extra.log`:
    logging.getLogger('extra').info("Hi there.")

    # This writes "UH OH" to `stderr` and to `./_log/app.log` (root logger):
    logging.getLogger().error("UH OH")

    # This writes "ho hum" to `./_log/app.log` only:
    logging.getLogger().debug("ho hum")


Using builtin formatters
++++++++++++++++++++++++++


Easily configuring a root logger
++++++++++++++++++++++++++++++++++

Adding a console handler
~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding a file handler
~~~~~~~~~~~~~~~~~~~~~~~~~~

Example
~~~~~~~~~~~~~~~~~~~~~~~~~~

A typical, useful approach is to add handlers to the root logger,
and then have each module log messages using ``logging.getLogger(__name__)``.
These "child" loggers require no configuration.


If the formatters of the handlers include the logger name — as does ``logger_level_msg``
of ``LoggingConfigDictEx`` objects, for example — each logged message will relate which module wrote it.


The following example illustrates the general technique:

    >>> from lcd import LoggingConfigDictEx
    >>> import logging
    >>> lcd_ex = LoggingConfigDictEx(add_handlers_to_root=True)
    >>> lcd_ex.add_stdout_console_handler('con', formatter='logger_level_msg')
    >>> lcd_ex.config()
    >>> logging.getLogger().warning("Look out!")
    root                : WARNING : Look out!
    >>> logging.getLogger('my_submodule').warning("Something wasn't right.")
    my_submodule        : WARNING : Something's was not right.
    >>> logging.getLogger('your_submodule').error("Uh oh, there was an error.")
    your_submodule      : ERROR   : Uh oh, there was an error.

.. note::
    The `logging` module supports a large number of keywords
    that can appear in formatters — for a complete list, see the documentation for
    `LogRecord attributes <https://docs.python.org/3/library/logging.html?highlight=logging#logrecord-attributes>`_.
    Each logged messages can even include the name of the function, and/or the line number,
    where its originating logging call was issued.



Configuring a non-root logger
++++++++++++++++++++++++++++++++++

non-root handler

Configuring both a root and a non-root logger
++++++++++++++++++++++++++++++++++++++++++++++++

root and non-root handler

--------------------------------------------------

Rotating file handlers
------------------------

rotating fh blah blah

--------------------------------------------------


Multiprocessing
-----------------

MP blather

Console handler, file handler, stream handler

--------------------------------------------------


Filters
--------

see tests ... for examples of how to set up a logger filter or a handler filter
