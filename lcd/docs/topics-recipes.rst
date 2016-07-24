Topics and Recipes
====================

.. include:: _global.rst

* ``LoggingConfigDict``
    .. hlist::
        :columns: 3

        * :ref:`Basic usage and principles<tr-basic-usage-LCD>`
        * :ref:`overview-example-using-only-LoggingConfigDict`

* ``LoggingConfigDictEx``
    * :ref:`tr-basic-LCDEx`

* Formatters
    .. hlist::
        :columns: 3

        * :ref:`tr-LCDEx-using-builtin-formatters`
        * :ref:`tr-LCDEx-defining-new-formatters`

* Configuring the root logger
    .. hlist::
        :columns: 3

        * :ref:`tr-easy-config-root-add-console`
        * :ref:`tr-easy-config-root-add-file`
        * :ref:`tr-config-root-use-children`

* Configuring and using root and non-root loggers together
    .. hlist::
        :columns: 3

        * :ref:`tr-config-non-root-propagate`
        * :ref:`tr-config-discrete-non-root`

* Rotating file handlers
    * :ref:`tr-rot-fh`

* Multiprocessing — using locking handlers
    .. hlist::
        :columns: 3

        * :ref:`tr-mp-console`
        * :ref:`tr-mp-fh`
        * :ref:`tr-mp-rot-fh`

* Filters
    .. hlist::
        :columns: 3

        * :ref:`tr-filters-logger`
        * :ref:`tr-filters-handler`

--------------------------------------------------

.. _tr-basic-usage-LCD:

Basic usage of ``LoggingConfigDict``
-------------------------------------------------------

.. todo::
    intro blather, basic usage of ``LoggingConfigDict``

Cite :ref:`LoggingConfigDict`: introduction for basic usage,
and reference // OR (todo): move that material to here.
???

The :ref:`overview` contains :ref:`an example <example-overview-config>` showing
how easy it is using ``LoggingConfigDictEx`` to
configure the root logger with both a console handler and a file handler.
The solution shown there takes advantage of a few conveniences provided by
``LoggingConfigDictEx``. It's instructive to see how the same result can be
achieved using only ``LoggingConfigDict``.

.. _overview-example-using-only-LoggingConfigDict:

The Overview example, using only ``LoggingConfigDict``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

If we were to use just the base class ``LoggingConfigDict``, the Overview example
becomes just a little less concise. Now, we have to add two formatters, and
we must explicitly add the two handlers to the root logger (two passages which
we've commented as ``# NEW``):

.. code::

    from lcd import LoggingConfigDict

    lcd = LoggingConfigDict(root_level='DEBUG')

    # NEW
    lcd.add_formatter('minimal',
                      format='%(message)s'
    ).add_formatter('logger_level_msg',
                    format='%(name)-20s: %(levelname)-8s: %(message)s'
    )

    lcd.add_handler('console',
                    formatter='minimal',
                    level='INFO',
                    class_='logging.StreamHandler',
    ).add_file_handler('file_handler',
                       formatter='logger_level_msg',
                       level='DEBUG',
                       filename='blather.log',
    )

    # NEW
    lcd.add_root_handlers('console', 'file_handler')

    lcd.config()


--------------------------------------------------

.. _tr-basic-LCDEx:

What ``LoggingConfigDictEx`` contributes
---------------------------------------------------------

.. todo::
    intro blather re  ``LoggingConfigDictEx``: why this superclass,
    what does it do, offer?

--------------------------------------------------

.. _tr-LCDEx-using-formatters:

Using formatters
-------------------------------------------------------

asfasdf

.. _tr-LCDEx-using-builtin-formatters:

Using builtin formatters
++++++++++++++++++++++++++
qwerty

.. _tr-LCDEx-defining-new-formatters:

Defining new formatters
++++++++++++++++++++++++++

The `logging` module supports a large number of keywords
that can appear in formatters — for a complete list, see the documentation for
`LogRecord attributes <https://docs.python.org/3/library/logging.html?highlight=logging#logrecord-attributes>`_.
Each logged message can even include the name of the function, and/or the line number,
where its originating logging call was issued.

--------------------------------------------------


.. _tr-easy-config-root:

Configuring the root logger
------------------------------------------

We already saw `one example <example-overview-config>` of how easy it is to
configure the root logger with both a console handler and a file handler.

.. _tr-easy-config-root-add-console:

Adding a console handler
++++++++++++++++++++++++++

.. _tr-easy-config-root-add-file:

Adding a file handler
++++++++++++++++++++++++++

.. _tr-config-root-use-children:

Using non-root (named, child) loggers without configuring them
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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


--------------------------------------------------

.. _tr-add-non-root:

Configuring and using non-root loggers
----------------------------------------------

Reasons to do so:

    * in a particular module or package, you want to use a different loglevel from
      that of the root logger, using the same handlers as the root (& so, writing
      to the same destination(s));

    * you want to write to destinations other than those of the root,
      either instead of or in addition to those.


.. _tr-config-non-root-propagate:

A propagating non-root logger
+++++++++++++++++++++++++++++++++++++++++++++++

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


.. _tr-config-discrete-non-root:

A "discrete" non-root logger
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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
and file handlers; use root loglevel ``'DEBUG'``; put logfiles in the ``_log/``
subdirectory of the current directory::

    import logging
    from lcd import LoggingConfigDictEx


    lcd_ex = LoggingConfigDictEx(log_path='_log/',
                                 root_level='DEBUG',
                                 add_handlers_to_root=True)

Set up the root logger with a ``stderr`` console handler and a file handler,
at their respective default loglevels ``'WARNING'`` and ``'NOTSET'``::

    lcd_ex.add_stderr_console_handler('console', formatter='minimal')
    lcd_ex.add_file_handler('root_fh',
                            filename='root.log',
                            formatter='logger_level_msg')

Add an ``'extra'`` logger, with loglevel ''`DEBUG`'',
which will write to a different file using a handler at default loglevel ``'NOTSET'``.
Note the use of parameters ``add_to_root`` and ``propagate``:

    * in the ``add_file_handler`` call, passing ``add_to_root=False`` ensures that
      this handler *won't* be added to the root logger,
      overriding the ``lcd_ex`` default value established by
      ``add_handlers_to_root=True`` above;

    * in the ``add_logger`` call, ``propagate=False`` ensures that messages logged
      by ``'extra'`` don't also write to the root and its handlers:

.. code::

        lcd_ex.add_file_handler('extra_fh',
                                filename='extra.log',
                                formatter='logger_level_msg',
                                add_to_root=False
                               )
        lcd_ex.add_logger('extra',
                          handlers=['extra_fh'],
                          level='DEBUG',
                          propagate=False
                         )

Finally, call ``config()`` to create actual objects of `logging` types —
``logging.Formatter``, ``logging.Logger``, etc. ::

    lcd_ex.config()

Now ``lcd_ex`` is actually no longer needed (we don't do 'incremental' configuration,
but then, arguably, neither does `logging`).

To use the loggers, access them by name::

    # 'extra' writes "Hi there" to file `_LOG/extra.log`:
    logging.getLogger('extra').warning("Hi there.")

    # Root writes "UH OH" to `stderr` and to `_LOG/root.log`:
    logging.getLogger().error("UH OH")

    # Root writes "ho hum" to `_LOG/root.log` only:
    logging.getLogger().debug("ho hum")

**Exercise**: Verify the claimed effects of the ``add_to_root`` and ``propagate``
parameters in the two calls that configure the ``'extra_fh'`` handler and the
``'extra'`` logger.

    1. Comment out ``add_to_root=False`` from the ``add_file_handler`` call
       for ``'extra_fh'``.

       Now, ``'extra_fh'`` is a handler of the root logger *too*, so
       it logs its messages ``"UH OH"`` and ``"ho hum"`` to ``_LOG/extra.log``,
       as well as to ``root.log`` and ``stderr`` as before.

       ``_LOG/root.log`` contains::

            root                : ERROR   : UH OH
            root                : DEBUG   : ho hum

       ``_LOG/extra.log`` contains::

            extra               : WARNING : Hi there.
            root                : ERROR   : UH OH
            root                : DEBUG   : ho hum

       ``stderr`` output::

            UH OH

    2. Uncomment ``add_to_root=False`` in the ``add_file_handler`` call,
       and comment out ``propagate=False`` from the ``add_logger`` call.

       Now, ``'extra'`` writes to the root's handlers as well as its own,
       so it logs a warning ``"Hi there."`` to both ``stderr`` and ``_LOG/root.log``.

       ``_LOG/root.log`` contains::

            extra               : WARNING : Hi there.
            root                : ERROR   : UH OH
            root                : DEBUG   : ho hum

       ``_LOG/extra.log`` contains::

            extra               : WARNING : Hi there.

       ``stderr`` output::

            Hi there.
            UH OH


.. _tr-propagate-docs:

.. index:: Logger.propagate property

.. index:: Placement of handlers when using multiple loggers, best practice

.. topic:: Best practices for propagation and handler placement

    According to the documentation for
    `Logger.propagate <https://docs.python.org/3/library/logging.html#logging.Logger.propagate>`_,


    | if [a logger's ``propagate`` property] evaluates to true [the default],
    | events logged to this logger will be passed to the handlers of higher level
    | (ancestor) loggers, in addition to any handlers attached to this logger.
    | Messages are passed directly to the ancestor loggers’ handlers - neither
    | the level nor filters of the ancestor loggers in question are considered.

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

.. _tr-rot-fh:

Using a rotating file handler
------------------------------------

rotating fh blah blah

--------------------------------------------------


.. _tr-mp:

Multiprocessing — using locking handlers
----------------------------------------------

(MP blather)

For a particular ``LoggingConfigDictEx``, there are two possibilities:

.. topic:: locking handlers used by default
    on every ``add_*_handler`` method call

    ``locking=True`` was passed to constructor

vs

.. topic:: standard handlers used by default
    on every ``add_*_handler`` method call

    ``locking=False`` was passed to constructor

    When you add (specs for) a handler using an ``add_*_handler`` method,
    pass ``locking=True`` to the method in order for the handler to be locking.


.. _tr-mp-console:

Using a locking console handler
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
123

.. _tr-mp-fh:

Using a locking file handler
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
abc

.. _tr-mp-rot-fh:

Using a locking rotating file handler
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
xyz

--------------------------------------------------


.. _tr-filters:

Filters
--------

see tests, test_LoggingConfigDict.py ...
for examples of how to set up a logger filter or a handler filter

``logging.Filter`` objects have a ``filter(record)`` method
which takes a ``logging.LogRecord`` and returns ``bool``.
In Py3, you can supply any callable ``LogRecord`` -> ``bool``
as a filter.
In Py2, you can supply anything that has ``.filter`` attribute,
and then, that attribute is *called* with a ``LogRecord``
and expected to return ``bool``.

The Py2 workaround: to use a function as a filter,
give it the attribute ``filter`` and let the value of that attribute
equal the function itself.


.. _filter-setup:

Defining filters
++++++++++++++++++++++++++++++++

Here are a couple of examples of filters. These never suppress
logging of a message, as they always return ``True``. Each has
side effects: printing messages, and incrementing a distinct
global variable::

    _info_count = 0
    _debug_count = 0

Classic filters are subclasses of logging.Filter::

    class CountInfoSquelchOdd(logging.Filter):
        def filter(self_, record):
            """Suppress odd-numbered messages (records) whose level == INFO,
            where the "first" message is the 0-th hence is even-numbered.
            :param self_: "self" for the CountInfo object (unused)
            :param record: logging.LogRecord
            :return: bool -- True ==> let record through, False ==> squelch
            """
            global _info_count
            if record.levelno == logging.INFO:
                _info_count += 1
                return _info_count % 2
            else:
                return True

A filter can also be a function::

    def count_debug_allow_2(record):
        """
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

    lcd_ex = LoggingConfigDictEx(
        add_handlers_to_root=True,
        root_level='DEBUG')

    lcd_ex.add_stdout_console_handler(
        'console',
        level='DEBUG',
        formatter='level_msg')

    lcd_ex.add_function_filter('count_d', count_debug_allow_2)
    lcd_ex.add_class_filter('count_i', CountInfoSquelchOdd)

    lcd_ex.add_root_filters('count_d', 'count_i')

    lcd_ex.config()

Now use the root logger::

    import logging
    root = logging.getLogger()

    # Py2: use u"Hi 1", etc.
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


Filters on a non-root logger
+++++++++++++++++++++++++++++

Adding the example filters to a non-root logger ``'mylogger'`` requires just one
change. Instead of using ``add_root_filters('count_d', 'count_i')`` to add the
filters to the root logger, add them when calling ``add_logger`` for ``'mylogger'``::

    lcd_ex.add_logger('mylogger',
                      filters=['count_d', 'count_i'],
                      ... )


Alternately, use [NEW< TODO] ``attach_logger_filters('mylogger',
                                                     'count_d', 'count_i')``
signature should be
    def attach_logger_filters(self, logger_name, *filter_names)
& similarly
    def attach_logger_handlers(self, logger_name, *handler_names)

.. _tr-filters-handler:

Filters on a handler
+++++++++++++++++++++++++++++

To add filters to a handler, use the ``filters`` keyword parameter to
**any** ``add_*_handler`` method. All such methods funnel through
``LoggingConfigDict.add_handler``. The ``filters`` parameter can be
either the name of a filter (a ``str``) or a sequence (``list``, ``tuple``, etc.)
of names of filters.

Using our two example filters, each of the following method calls adds a handler
with just the ``'count_d'`` filter attached::

    lcd_ex.add_stderr_console_handler('con-err',
                                      filters='count_d')
    lcd_ex.add_file_handler('fh',
                            filename='some-logfile.log',
                            filters=['count_d'])

The following statement adds a rotating file handler with both filters attached::

    lcd_ex.add_rotating_file_handler('rfh',
                                     filename='some-rotating-logfile.log',
                                     max_bytes=1024,
                                     backup_count=5,
                                     filters=['count_i', 'count_d'])
