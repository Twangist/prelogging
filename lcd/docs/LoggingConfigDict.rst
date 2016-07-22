.. _LoggingConfigDict:

LoggingConfigDict
===============================

This class resides in ``logging_config_dict.py``.

As shown in the Introduction's :ref:`class inheritance diagram <lcd-all-classes>`,
objects of this class *are* dicts — *logging config dicts*.

.. automodule:: lcd.logging_config_dict


.. autoclass:: lcd.logging_config_dict.LoggingConfigDict
    :members: __init__, formatters, filters, handlers, loggers, root, set_root_level,
              add_filter, add_formatter, add_handler, add_logger, add_root_filters, add_root_handlers,
              add_file_handler, set_handler_level, set_logger_level, config, dump
    :special-members:
