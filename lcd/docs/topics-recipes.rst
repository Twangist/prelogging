Topics and Recipes
====================

.. include:: _global.rst

.. todo::
    Blah examples/topics blah

--------------------------------------------------

Basic usage of ``LoggingConfigDict``
-------------------------------------------------------


.. todo::
    intro blather, basic usage of ``LoggingConfigDict``

--------------------------------------------------

Basic usage of ``LoggingConfigDictEx``
---------------------------------------------------------

.. todo::
    intro blather, basic usage of ``LoggingConfigDictEx``

EXAMPLE -- Adding a logger that's discrete from the root (or any parent)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

8980 7606 2417

.. todo::
    Explain the heading a bit

Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Root logger with a ``stderr`` console handler and a file handler,
at their respective `lcd` default loglevels ``'WARNING'`` and ``'NOTSET'``;

a discrete logger, named let's say ``'extra'``, with loglevel ''`DEBUG`'',
which will write to a different file using a handler at default loglevel ``'NOTSET'``.

How to realize them [sic?]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start with a ``LoggingConfigDictEx`` that uses standard (non-locking) stream
and file handlers. Put logfiles in the ``_log/`` subdirectory of the current
directory. Use root loglevel ``'DEBUG'``. ::

    import logging
    from lcd import LoggingConfigDictEx


    lcd_ex = LoggingConfigDictEx(log_path='_log/',
                                 root_level='DEBUG',
                                 add_handlers_to_root=True)

Set up the root logger with a ``stderr`` console handler and a file handler,
at their respective default loglevels ``'WARNING'`` and ``'NOTSET'``::

    lcd_ex.add_stderr_console_handler('console', formatter='minimal')
    lcd_ex.add_file_handler('app_fh',
                            filename='app.log',
                            formatter='logger_level_msg')

Add an ``'extra'`` logger, with loglevel ''`DEBUG`'',
which will write to a different file using a handler at default loglevel ``'NOTSET'``.
Note the use of parameters ``add_to_root`` and ``propagate``:

    * ``add_to_root=False`` ensures that this handler *won't* be added to the root logger,
      overriding the ``lcd_ex`` default value established by ``add_handlers_to_root=True`` above;

    * ``propagate=False`` ensures that messages logged by ``'extra'``
      don't also write to the root and its handlers:

.. code::

        lcd_ex.add_file_handler('extra_fh',
                                filename='app_extra.log',
                                formatter='logger_level_msg',
                                add_to_root=False)
        lcd_ex.add_logger('extra',
                          handlers=['extra_fh'],
                          level='DEBUG',
                          propagate=False)

Finally, call ``config()`` to create actual objects of `logging` types — ``logging.Formatter``,
``logging.Logger``, etc. ::

    lcd_ex.config()

Now ``lcd_ex`` is actually no longer needed (we don't do 'incremental' configuration,
but then, arguably, neither does `logging`).

To use the loggers, access them by name::

    # This writes "Hi there" to file `_LOG/app_extra.log`:
    logging.getLogger('extra').warning("Hi there.")

    # This writes "UH OH" to `stderr` and to `_LOG/app.log` (root logger):
    logging.getLogger().error("UH OH")

    # This writes "ho hum" to `_LOG/app.log` only:
    logging.getLogger().debug("ho hum")

**Exercise**: Verify the claimed effects of the ``add_to_root`` and ``propagate`` parameters
in the calls that configure the ``'extra'`` logger.

    1. Omit ``add_to_root=False`` from the ``add_file_handler`` call.
       Observe that ``"Hi there."`` gets logged to ``stderr`` and to ``_LOG/app.log``
       by logger ``'extra'``.

    2. Restore ``add_to_root=False`` to the ``add_file_handler`` call,
       and omit ``propagate=False`` from the ``add_logger`` call.
       Observe that ``"UH OH"`` and ``"ho hum"`` are logged to ``_LOG/app_extra.log``
       by the root logger.


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
These "child" loggers require no configuration; they use the handlers
of the root because by default loggers are created with ``propagate=True``.

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

Console handler (MP)
+++++++++++++++++++++++++++++
123

File handler (MP)
+++++++++++++++++++++++++++++
abc

Rotating file handler (MP)
+++++++++++++++++++++++++++++
xyz

--------------------------------------------------


Filters
--------

see tests ... for examples of how to set up a logger filter or a handler filter
