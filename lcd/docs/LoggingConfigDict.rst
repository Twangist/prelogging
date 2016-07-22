.. _LoggingConfigDict:

LoggingConfigDict
===============================

This class resides in ``logging_config_dict.py``.

As shown in the Introduction's :ref:`class inheritance diagram <lcd-all-classes>`,
objects of this class *are* dicts — *logging config dicts*.
The methods of this class —``add_formatter``, ``add_filter``,
``add_handler``, ``add_logger``, and so on — operate on the underlying dictionary.
That dict is significantly nested, and keys often appear among the data, as
back references to things "already defined".

Although dicts are unordered, when configuring logging there's a precedence ordering
for specifying objects:

    1. Create a ``LoggingConfigDict``, optionally specifying the level of the root handler.

    2. Add formatter specifications with ``add_formatter()``.

    3. Add any filter specifications with ``add_filter()``.

    4. Add handler specifications with ``add_handler()`` and/or ``add_file_handler()``,
       referring by name to formatters and filters already specified in previous steps.

    *In steps 2. – 4. you give each thing specified a name, by which you refer to it
    in subsequent steps when associating the thing with other, higher-level things.*

    5. If desired, configure the root logger using ``add_root_handlers()``, ``add_root_filters()``
       and/or ``set_root_level()``, referring by name to handlers and filters already specified
       in previous steps.

    6. Add specifications for any non-root loggers with ``add_logger()``.
       Specify the handlers and filters of a logger by name, using the ``handlers``
       and ``filters`` keyword parameters.

    *Steps 2. and 3. can be interchanged, likewise Steps 5. and 6.*

A single ``LoggingConfigDict`` can be passed around to different "areas" of a program,
each contributing specifications of its desired formatters, filters, handlers and
loggers. 

Once a ``LoggingConfigDict`` has been populated, it can be used to configure
logging by calling its ``config()`` method, which is basically just shorthand
for a call to
`logging.config.dictConfig() <https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig>`_.



.. autoclass:: lcd.logging_config_dict.LoggingConfigDict
    :members: __init__, formatters, filters, handlers, loggers, root, set_root_level,
              add_filter, add_formatter, add_handler, add_logger, add_root_filters, add_root_handlers,
              add_file_handler, set_handler_level, set_logger_level, config, dump
    :special-members:
