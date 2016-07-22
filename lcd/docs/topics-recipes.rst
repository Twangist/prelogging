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


Using formatters
++++++++++++++++++++++++++

asfasdf

Using builtin formatters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
qwerty

Defining new formatters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
    The `logging` module supports a large number of keywords
    that can appear in formatters — for a complete list, see the documentation for
    `LogRecord attributes <https://docs.python.org/3/library/logging.html?highlight=logging#logrecord-attributes>`_.
    Each logged message can even include the name of the function, and/or the line number,
    where its originating logging call was issued.


Easily configuring a root logger
++++++++++++++++++++++++++++++++++

Adding a console handler
~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding a file handler
~~~~~~~~~~~~~~~~~~~~~~~~~~

Example [TODO: of WHAT?]
~~~~~~~~~~~~~~~~~~~~~~~~~~

A typical, useful approach is to add handlers only to the root logger,
and then have each module log messages using ``logging.getLogger(__name__)``.
These "child" loggers require no configuration; they use the handlers
of the root because by default loggers are created with ``propagate=True``.

If the formatters of the handlers include the logger name — as does ``logger_level_msg``
of ``LoggingConfigDictEx`` objects, for example — each logged message will relate
which module wrote it.

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


Adding non-root loggers
----------------------------------

Reasons to do so:

    * in a particular module or package, you want to use a different loglevel from
      that of the root logger, using the same handlers as the root (& so, writing
      to the same destination(s));

    * you want to write to destinations other than those of the root,
      either instead of or in addition to those.


Configuring a non-root logger
++++++++++++++++++++++++++++++++++

.. todo:: this.

One which propagates, and (two possibilities)

    1. has no handlers of its own, or
    2. has handlers of its own

Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
asdf

How-to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fdsa


Using the root logger and a "discrete" logger
+++++++++++++++++++++++++++++++++++++++++++++++

In this example we use two loggers: the root, and another logger that's "discrete"
from the root, and indeed from any ancestor logger, in the sense that:

    * it doesn't share any handlers with any ancestor, and
    * it doesn't propagate to any ancestor.

As the root is an ancestor of every logger, in particular we'll require that
the added logger should *not* add its handlers to the root, and that it should
not "propagate" to its parent (the root, in this example).


Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Root logger with a ``stderr`` console handler and a file handler,
at their respective `lcd` default loglevels ``'WARNING'`` and ``'NOTSET'``;

a discrete logger, named let's say ``'extra'``, with loglevel ''`DEBUG`'',
which will write to a different file using a handler at default loglevel ``'NOTSET'``.

How-to
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

.. _blahblah:

.. index:: Logger.propagate property

.. index:: Placement of handlers when using multiple loggers, best practice

.. note::
    According to the documentation of the
    `Logger.propagate property <https://docs.python.org/3/library/logging.html#logging.Logger.propagate>`_,


    | if [``propagate``] evaluates to true [the default], events logged
    | to this logger will be passed to the handlers of higher level (ancestor)
    | loggers, in addition to any handlers attached to this logger. Messages
    | are passed directly to the ancestor loggers’ handlers - neither the level
    | nor filters of the ancestor loggers in question are considered.

    |br|
    This suggests that truly intricate, and no doubt surprising, configurations
    can be achieved using propagation and fussy placements of handlers on loggers.
    The **Note** at the end of the above link clearly states best practice:

    | If you attach a handler to a logger and one or more of its ancestors,
    | it may emit the same record multiple times. In general, you should not
    | need to attach a handler to more than one logger - if you just attach it
    | to the appropriate logger which is highest in the logger hierarchy, then
    | it will see all events logged by all descendant loggers, provided that
    | their propagate setting is left set to True. A common scenario is to
    | attach handlers only to the root logger, and to let propagation take care
    | of the rest.

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
