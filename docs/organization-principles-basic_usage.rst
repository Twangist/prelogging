Organization, Principles and Basic Usage
=========================================

.. include:: _global.rst

* ``LCD``
    .. hlist::
        :columns: 3

        * :ref:`Basic usage and principles<basic-usage-LCD>`
        * :ref:`overview-example-using-only-LCD`

* ``LCDEx``
    * :ref:`basic-LCDEx`

* Formatters
    .. hlist::
        :columns: 3

        * :ref:`defining-new-formatters`
        * :ref:`LCDEx-using-formatter-presets`

* Adding handlers
    .. hlist::
        :columns: 3

        * :ref:`add-console-handler`
        * :ref:`add-file-handler`
        * :ref:`add-other-handler`

* Configuring the root logger
    .. hlist::
        :columns: 3

        * :ref:`config-root-basic`
        * :ref:`config-root-use-children`

* Configuring non-root loggers; using root and non-root loggers together
    .. hlist::
        :columns: 3

        * :ref:`config-non-root-propagate`
        * :ref:`config-discrete-non-root`


* :ref:`warnings-consistency-checking`
    .. hlist::
        :columns: 3

        * :ref:`lcd-warnings`
        * :ref:`check`


--------------------------------------------------

.. _basic-usage-LCD:

``LCD``
-------------------------------------------------------

<<< NOTE NOTE NOTE  lcd.logging_config_dict docstring  NOTE NOTE NOTE >>>

``LCD`` provides an API for building dictionaries that specify
Python logging configuration -- *logging config dicts*.

Entering a logging config dict as static data requires many nested curly
braces, colons, single-quoted keywords, and boilerplate default key/value pairs.
Such dicts are significantly nested, and keys often appear among
the data, as back-references to things "already defined".

But logging configuration involves a small hierarchy of only four kinds of
entities — formatters, handlers, loggers and, optionally, filters —
which can be specified in a layered way.

``LCD`` lets you build a logging config dict modularly and
incrementally. It flattens the process of specifying the dict, letting you
define each entity one by one, instead of entering a thicket of nested dicts.

An ``LCD`` instance *is* a logging config dict. It inherits from
``dict``, and its methods —``add_formatter``, ``add_handler``, ``add_logger``,
and so on — operate on the underlying dictionary, breaking down the process
of creating a logging config dict into basic steps:

    1. Create an ``LCD``, optionally specifying the level of
       the root handler.

    2. Add formatter specifications with ``add_formatter()``.

    3. Add any filter specifications with ``add_filter()``.

    4. Add handler specifications with ``add_handler()`` and/or
       ``add_file_handler()``: for each filter, specify its name, formatter,
       and loglevel, and and optionally attach filters. Formatters and filters
       are specified by name, so they should already have been added in previous
       steps (if they weren't, by default `lcd` will issue a warning). Although
       you can provide all these attributes of a handler in the
       ``add_*_handler`` call, you can do so later, after the basic call: other
       methods let you attach a formatter, attach filters, and set the handler's
       loglevel.

    *In steps 2. – 4. you give each specified entity a name, by which you refer
    to it subsequently when modifying it or attaching it to other, higher-level
    entities.*

    5. If desired, configure the root logger using ``attach_root_handlers()``,
       ``attach_root_filters()`` and/or ``set_root_level()``, referring by name
       to handlers and filters already specified in previous steps.

    6. Add specifications for any non-root loggers with ``add_logger()``.
       Specify the handlers and filters of a logger by name, using the
       ``handlers`` and ``filters`` keyword parameters. You can also attach
       handlers and filters to an already-added logger, and set its loglevel.

    *Steps 2. and 3. can be interchanged, likewise 5. and 6.*

Keyword parameters of the ``add_*`` methods are, with a few, documented exceptions,
the very same keys that occur in the configuring dictionaries of the corresponding
kind of logging entities (with just one exception: ``class_`` instead of
``class``). For example, the keyword parameters of ``add_file_handler`` are
keys that can appear in a dictionary of configuration settings for a file handler;
the keyword parameters of ``add_logger`` are keys that can appear in a dict that
configures a logger. In any case, all receive sensible default values consistent
with `logging`.

Once you've built an ``LCD`` meeting your requirements, you
configure logging by calling the object's ``config`` method, which
passes itself (a dict) to
`logging.config.dictConfig() <https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig>`_.


Methods, terminology
+++++++++++++++++++++

Here's what a minimal, "blank" logging config dict looks like::

    >>> from lcd import LCD
    >>> d = LCD()
    >>> d.dump()        # prettyprint the underlying dict
    {'filters': {},
     'formatters': {},
     'handlers': {},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': [], 'level': 'WARNING'},
     'version': 1}

Every logging config dict built by `lcd` has the five subdictionaries shown.
The ``LCD`` class exposes them as properties:
``formatters``, ``filters``, ``handlers``, ``loggers``, ``root``.
``root`` is a dict containing settings for that special logger. Every other
subdict contains keys that are names of entities of the appropriate kind;
the value of each such key is a dict containing configuration settings for
the entity. In an alternate universe, ``'root'`` and its value (the ``root``
subdict) could be just a special item in the ``loggers`` subdict; but
logging config dicts aren't defined that way.


The ``add_*`` methods
~~~~~~~~~~~~~~~~~~~~~~~

The four basic ``add_*`` methods are::

    add_formatter(self, name, format='', ... )
    add_filter(self, name, ... )
    add_handler(self, name, level='NOTSET', formatter=None, filters=None, ... )
    add_logger(self, name, level='NOTSET', handlers=None, filters=None, ...  )

``LCD`` also defines two special cases of ``add_handler``: ``add_file_handler``
and ``add_null_handler``.

Each ``add_*`` method adds an item to (or replaces an item in) the corresponding
subdict. When you add a formatter::

    >>> _ = d.add_formatter('fmtr', format="%(name)s %(message)s")

you add an item to ``d.formatters``, whose key is ``'fmtr'`` and whose value is
a dict with the given settings::

    >>> d.dump()
    {'filters': {},
     'formatters': {'fmtr': {'class': 'logging.Formatter',
                             'format': '%(name)s %(message)s'}},
     'handlers': {},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': [], 'level': 'WARNING'},
     'version': 1}

The result is as if you had executed::

    d.formatters['fmtr'] = {'class': 'logging.Formatter',
                            'format': '%(name)s %(message)s'}

Now, when you add a handler, you can assign this formatter to it by name::

    >>> _ = d.add_file_handler('fh', filename='logfile.log', formatter='fmtr')

This ``add_*_handler`` method added an item to ``d.handlers`` — a specification
for a new handler ``'fh'``::

    >>> d.dump()
    {'filters': {},
     'formatters': {'fmtr': {'class': 'logging.Formatter',
                             'format': '%(name)s %(message)s'}},
     'handlers': {'fh': {'class': 'logging.FileHandler',
                         'delay': False,
                         'filename': 'logfile.log',
                         'formatter': 'fmtr',
                         'level': 'NOTSET',
                         'mode': 'w'}},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': [], 'level': 'WARNING'},
     'version': 1}

Similarly, ``add_filter`` and ``add_logger`` add items to the ``filters`` and
``loggers`` dictionaries.

The ``attach_*_*`` methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The configuring dict of a handler has an optional ``'filters'`` list;
the configuring dict of a logger can have a ``'filters'`` list and/or
a ``'handlers'`` list. The ``attach_``\ *entity*\ ``_``\ *entities* methods
extend these filters and handlers collections::

    attach_handler_filters(self, handler_name, * filter_names)

    attach_logger_handlers(self, logger_name, * handler_names)
    attach_logger_filters(self, logger_name, * filter_names)

    attach_root_handlers(self, * handler_names)
    attach_root_filters(self, * filter_names)

To illustrate, Let's add another handler, attach both handlers to the root,
and examine the underlying dict::

    >>> _ = d.add_handler('console',
    ...                   formatter='fmtr',
    ...                   level='INFO',
    ...                   class_='logging.StreamHandler'
    ... ).attach_root_handlers('fh', 'console')
    >>> d.dump()
    {'filters': {},
     'formatters': {'fmtr': {'class': 'logging.Formatter',
                             'format': '%(name)s %(message)s'}},
     'handlers': {'console': {'class': 'logging.StreamHandler',
                              'formatter': 'fmtr',
                              'level': 'INFO'},
                  'fh': {'class': 'logging.FileHandler',
                         'delay': False,
                         'filename': 'logfile.log',
                         'formatter': 'fmtr',
                         'level': 'NOTSET',
                         'mode': 'w'}},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': ['fh', 'console'], 'level': 'WARNING'},
     'version': 1}

The ``set_*_*`` methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~

These methods modify a single value -- a loglevel, or a formatter (the outlier
case)::

    set_handler_level(self, handler_name, level)
    set_root_level(self, root_level)
    set_logger_level(self, logger_name, level)
    set_handler_formatter(self, handler_name, formatter_name)

We might have named the last method "attach_handler_formatter", as the
handler-formatter relation is another example of an association between two
different kinds of logging entities. However, further reflection reveals that
a formatter is not "attached" in the sense of all the other "attach_*"
methods. A handler has at most one formatter, and "setting" a handler's
formatter replaces any formatter previously set; whereas the attach methods
only append to and extend collections of filters and handlers, they never delete
or replace items. Hence "set_handler_formatter".

``__init__``
~~~~~~~~~~~~~~~~~~

discuss its parameters here?
or discuss two ::

    root_level='WARNING',              # == logging default
    disable_existing_loggers=None,     # logging default: True

``root_level`` -- the `lcd` default is the `logging` default.
This can also be set with ``set_root_level`` method.

TWO WAYS TO DO THIS. <<<<<<------------- is that good?


``disable_existing_loggers``:
the ``LCD`` default of ``None`` uses the `logging` default (``True``)
for ``disable_existing_loggers``.
This can also be set as a parameter to ``config``.


TODO TODO TODO Maybe make this a property??????? a r/w property....
Reads -- from dict;
writes -- to dict :)

and dispense with it as a parameter to config (that's silly, no?)


TWO WAYS TO DO THIS. <<<<<<------------- is that good?

``warnings``: point to discussion of "warnings"


Other methods
~~~~~~~~~~~~~~~~~~
::

    dump()
    check(self, verbose=True)
    config(...)


.. _overview-example-using-only-LCD:

The Overview example, using only ``LCD``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The :ref:`overview` contains :ref:`an example <example-overview-config>` showing
how easy it is using ``LCDEx`` to
configure the root logger with both a console handler and a file handler.
The solution shown there takes advantage of a few conveniences provided by
``LCDEx``. It's instructive to see how the same result can be
achieved using only ``LCD`` and forgoing the conveniences of ``LCDEx``.


If we were to use just the base class ``LCD``, the Overview
example becomes just a little less concise. Now, we have to add two formatters,
and we must explicitly attach the two handlers to the root logger (two passages
which we've commented as ``# NEW``):

.. code::

    from lcd import LCD

    lcd = LCD(root_level='DEBUG')

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
    lcd.attach_root_handlers('console', 'file_handler')

    lcd.config()


--------------------------------------------------

.. _basic-LCDEx:

``LCDEx``
----------

``LCDEx`` is a subclass of ``LCD`` which contributes additional conveniences:

* formatter presets;
* optional automatic attaching of handlers to the root logger
  as they're added (/"defined"/specified/configured...);
* easy use of the "locking" (multiprocessing-safe) handler classes
  that `lcd` provides;
* simplified filter creation;
* various ``add_*_handler`` methods for configuring handlers of several
  `logging` handler classes, with optional locking support in most cases:

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

Except for properties and the ``__init__`` method, all public instance
methods of this class return ``self``.


.. _LCDEx-init-params:

.. index:: __init__ keyword parameters (LCDEx)

``__init__`` keyword parameters
++++++++++++++++++++++++++++++++++++++++++

In addition to the parameters ``root_level``,
``disable_existing_loggers`` and ``warnings`` recognized by :ref:`LCD`,
the constructor of this class accepts a few more::

        log_path                (str)
        attach_handlers_to_root (bool)
        locking                 (bool)

``log_path`` is a directory in which log files will be created by
``add_file_handler`` and ``add_rotating_file_handler``. If the filename
passed to those methods contains a relative path, then the logfile will
be created in that relative subdirectory of ``log_path``. If ``log_path``
is not an absolute path, then it is relative to the current directory
at runtime when ``config()`` is finally called.

When ``attach_handlers_to_root`` is true [default: False], by default the
other methods of this class automatically add handlers to the root logger
as well as to the ``handlers`` subdictionary. Each instance saves the
value passed to its constructor, and exposes it as the read-only property
``attach_handlers_to_root``.

When ``locking`` is true [default: False], by default the other methods of
this class add :ref:`locking handlers <locking-handlers>`; if it's false,
handlers instantiate the "usual" classes defined by `logging`. (See the
:ref:`class inheritance diagram <lcd-all-classes>`.) Each instance saves the
value passed to its constructor, and exposes it as the read-only property
``locking``.

All of the methods that add a handler take parameters ``attach_to_root``
and ``locking``, each a ``bool`` or ``None``; these allow overriding of
the values passed to the constructor. Thus, for example, callers can
add a non-locking handler even if ``self.locking`` is true, or a locking
handler even if ``self.locking`` is false. The default value of these
parameters in handler-adding methods is ``None``, meaning: use the
corresponding value passed to the constructor.

.. _LCDEx-handler-classes-encapsulated:

.. index:: `'logging` handler classes encapsulated

.. _preset-formatters:

.. index:: preset formatters (LCDEx), formatter presets (LCDEx)

Formatter presets
+++++++++++++++++++++++++++++

Their names make it fairly obvious what their format strings are:

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


--------------------------------------------------

.. _using-formatters:

Using formatters
-------------------------------------------------------

<<<<< TODO >>>>> 

.. _defining-new-formatters:

Defining new formatters
++++++++++++++++++++++++++
todo BLA BLAH BLAHH


Setting the format string
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

todo BLA BLAH BLAHH

The `logging` module supports a large number of keywords
that can appear in formatters — for a complete list, see the documentation for
`LogRecord attributes <https://docs.python.org/3/library/logging.html?highlight=logging#logrecord-attributes>`_.
Each logged message can even include the name of the function, and/or the
line number, where its originating logging call was issued.

`logging` parameter names are all over the place. The ``Formatter`` class uses
``fmt`` for the name of this parameter; static configuration uses ``format``.
We allow both ``fmt`` and ``format``. If both ``format`` and ``fmt`` are given,
``format`` takes precedence.

Selecting [SIC] the style of the format string (Python 3 only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``style`` parameter to ``Formatter.__init__`` lets you use any of
Python's three format styles in the format string used by a ``Formatter``.
Although the documentation for logging configuration doesn't mention it,
``style`` also works in Python 3 logging config dicts.

The value of ``style`` can be one of the following:

|    ``'%'``     old-style, ``%``-based formatting (the default)
|    ``'{'``     new-style formatting, using ``str.format``
|    ``'$'``     template-based formatting

A little example:

    >>> import lcd
    >>> import logging
    >>> lcdx = lcd.LCDEx(attach_handlers_to_root=True)
    # >>> lcdx.add_formatter('testform', format='{levelname} {name} {message}', style='{')
    >>> lcdx.add_formatter('testform', format='%(levelname)s %(name)s %(message)s', style='%')
    >>> lcdx.add_stderr_handler('con', formatter='testform')
    >>> lcdx.config()
    >>> root = logging.getLogger()
    >>> root.warning('Hi there')
    WARNING Hi there

Setting the date/time format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. todo::    blah blah? more?
    
The dateformat (alias datefmt) parameter specifies a format string for dates
and times, with the same keys accepted by 
`time.strftime <https://docs.python.org/3/library/time.html#time.strftime>`_.        
If both ``datefmt`` and ``dateformat`` are given, ``datefmt`` takes precedence.


.. _LCDEx-using-formatter-presets:

Using formatter presets
++++++++++++++++++++++++++
<<<<< TODO >>>>>

.. topic:: Adding formatter presets (todo -- this too)

    You can do this. <SAY briefly why you might want to.> See
    :ref:`adding-new-formatter-presets` for details.

--------------------------------------------------

.. _adding-handlers:

Adding handlers
--------------------

.. _add-console-handler:

Adding a console handler
++++++++++++++++++++++++++
<<<<< TODO >>>>>

.. _add-file-handler:

Adding a file handler
++++++++++++++++++++++++++
<<<<< TODO >>>>>

.. _add-other-handler:

Adding other kinds of handlers
+++++++++++++++++++++++++++++++++
<<<<< TODO -- refer to list above of what LCDEx adds, and to topics-recipes chapter >>>>>



--------------------------------------------------

.. _easy-config-root:

Configuring the root logger
------------------------------------------

We already saw :ref:`one example <example-overview-config>` of how easy it is to
configure the root logger with both a console handler and a file handler.

.. _config-root-basic:

Basic usage: attaching handlers
+++++++++++++++++++++++++++++++++++

<<<< TODO blah^2 >>>>

.. _config-root-use-children:

Using non-root loggers without configuring them
++++++++++++++++++++++++++++++++++++++++++++++++

A common, useful approach is to attach handlers only to the root logger,
and then have each module log messages using ``logging.getLogger(__name__)``.
These "child" loggers require no configuration; they use the handlers
of the root because, by default, loggers are created with ``propagate=True``.

If the formatters of the handlers include the logger name — as does
``logger_level_msg`` of ``LCDEx`` objects, for example — each
logged message will relate which module wrote it.

The following example illustrates the general technique:

    >>> from lcd import LCDEx
    >>> import logging
    >>> lcd_ex = LCDEx(attach_handlers_to_root=True)
    >>> lcd_ex.add_stdout_handler('con', formatter='logger_level_msg')
    >>> lcd_ex.config()

    >>> logging.getLogger().warning("Look out!")
    root                : WARNING : Look out!
    >>> logging.getLogger('my_submodule').warning("Something wasn't right.")
    my_submodule        : WARNING : Something's wasn't right.
    >>> logging.getLogger('your_submodule').error("Uh oh, there was an error.")
    your_submodule      : ERROR   : Uh oh, there was an error.


--------------------------------------------------

.. _add-non-root:

Configuring and using non-root loggers
----------------------------------------------

Reasons to do so:

    * in a particular module or package, you want to use a different loglevel
      from that of the root logger, using the same handlers as the root (& so,
      writing to the same destination(s));

    * you want to write to destinations other than those of the root,
      either instead of or in addition to those.


.. _config-non-root-propagate:

A propagating non-root logger
+++++++++++++++++++++++++++++++++++++++++++++++

.. todo:: this.

One which propagates. There are two possibilities:

    1. the non-root logger has no handlers attached;
    2. the non-root logger has handlers attached.

Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<<<<< TODO >>>>> 

How-to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<<<<< TODO >>>>> 


.. _config-discrete-non-root:

A "discrete" non-root logger
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

In this example we use two loggers: the root, and another logger that's
"discrete" from the root, and indeed from any ancestor logger, in the sense
that:

    * it doesn't share any handlers with any ancestor, and
    * it doesn't propagate to any ancestor.

As the root is an ancestor of every logger, in particular we'll require that
the added logger should *not* attach its handlers to the root, and that it
should not "propagate" to its parent (the root, in this example).


Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Root logger with a ``stderr`` console handler and a file handler,
at their respective `lcd` default loglevels ``'WARNING'`` and ``'NOTSET'``;

a discrete logger, named let's say ``'extra'``, with loglevel ''`DEBUG`'',
which will write to a different file using a handler at default loglevel
``'NOTSET'``.

How-to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start with a ``LCDEx`` that uses standard (non-locking) stream
and file handlers; use root loglevel ``'DEBUG'``; put logfiles in the ``_log/``
subdirectory of the current directory::

    import logging
    from lcd import LCDEx


    lcd_ex = LCDEx(log_path='_log/',
                   root_level='DEBUG',
                   attach_handlers_to_root=True)

Set up the root logger with a ``stderr`` console handler and a file handler,
at their respective default loglevels ``'WARNING'`` and ``'NOTSET'``::

    lcd_ex.add_stderr_handler('console', formatter='msg')
    lcd_ex.add_file_handler('root_fh',
                            filename='root.log',
                            formatter='logger_level_msg')

Add an ``'extra'`` logger, with loglevel ''`DEBUG`'', which will write to a
different file using a handler at default loglevel ``'NOTSET'``.
Note the use of parameters ``attach_to_root`` and ``propagate``:

    * in the ``add_file_handler`` call, passing ``attach_to_root=False`` ensures
      that this handler *won't* be attached to the root logger, overriding the
      ``lcd_ex`` default value established by ``attach_handlers_to_root=True``
      above;

    * in the ``add_logger`` call, ``propagate=False`` ensures that messages
      logged by ``'extra'`` don't also write to the root and its handlers:

.. code::

        lcd_ex.add_file_handler('extra_fh',
                                filename='extra.log',
                                formatter='logger_level_msg',
                                attach_to_root=False)
        lcd_ex.add_logger('extra',
                          handlers=['extra_fh'],
                          level='DEBUG',
                          propagate=False)

Finally, call ``config()`` to create actual objects of `logging` types —
``logging.Formatter``, ``logging.Logger``, etc. ::

    lcd_ex.config()

Now ``lcd_ex`` is actually no longer needed (we don't do 'incremental'
configuration, but then, arguably, neither does `logging`).

To use the loggers, access them by name::

    # 'extra' writes "Hi there" to file `_LOG/extra.log`:
    logging.getLogger('extra').warning("Hi there.")

    # Root writes "UH OH" to `stderr` and to `_LOG/root.log`:
    logging.getLogger().error("UH OH")

    # Root writes "ho hum" to `_LOG/root.log` only:
    logging.getLogger().debug("ho hum")

**Exercise**: Verify the claimed effects of the ``attach_to_root`` and
``propagate`` parameters in the two calls that configure the ``'extra_fh'``
handler and the ``'extra'`` logger.

    1. Comment out ``attach_to_root=False`` from the ``add_file_handler`` call
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

    2. Uncomment ``attach_to_root=False`` in the ``add_file_handler`` call,
       and comment out ``propagate=False`` from the ``add_logger`` call.

       Now, ``'extra'`` writes to the root's handlers as well as its own,
       so it logs a warning ``"Hi there."`` to both ``stderr`` and
       ``_LOG/root.log``.

       ``_LOG/root.log`` contains::

            extra               : WARNING : Hi there.
            root                : ERROR   : UH OH
            root                : DEBUG   : ho hum

       ``_LOG/extra.log`` contains::

            extra               : WARNING : Hi there.

       ``stderr`` output::

            Hi there.
            UH OH


.. _propagate-docs:

.. index:: Logger.propagate property
.. index:: Propagation — best practices
.. index:: Placement of handlers when using multiple loggers — best practices

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
    can be achieved using propagation and fussy placements of handlers on
    loggers. The **Note** at the end of the above link clearly states best
    practice:

    | If you attach a handler to a logger and one or more of its ancestors,
    | it may emit the same record multiple times. In general, you should not
    | need to attach a handler to more than one logger - if you just attach it
    | to the appropriate logger which is highest in the logger hierarchy, then
    | it will see all events logged by all descendant loggers, provided that
    | their propagate setting is left set to True. A common scenario is to
    | attach handlers only to the root logger, and to let propagation take care
    | of the rest.

--------------------------------------------------

.. _warnings-consistency-checking:

`lcd` warnings and consistency checking
-----------------------------------------------------------

Added benefit provided by `lcd` that you don't enjoy by handing a big
hand-coded dict to `logging.config.dictConfig()``.

`lcd` detects certain dubious practices, automatically corrects some of them
and optionally prints warnings about them.

In addition, the ``check`` method ........ BLAH BLAH .......

.. _lcd-warnings:

`lcd` warnings
+++++++++++++++

(blah blah...)

The inner class ``LCD.Warnings``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``LCD`` has an inner class ``Warnings`` which defines bit-field "constants"
that indicate the different kinds of anomalies that `lcd` checks for, corrects
when that's sensible, and optionally reported on with warning messages.

+--------------------------+-------------------------------------------------------------+
|| ``Warnings`` "constant" || Issue a warning when...                                    |
+==========================+=============================================================+
|| ``REATTACH``            || attaching an entity {formatter/filter/handler}             |
||                         || to another entity that it's already attached to            |
|| ``REDEFINE``            || overwriting an existing definition of an entity            |
|| ``REPLACE_FORMATTER``   || changing a handler's formatter                             |
|| ``UNDEFINED``           || attaching an entity that hasn't yet been added ("defined") |
+--------------------------+-------------------------------------------------------------+

The class also defines a couple of shorthand "constant"::

    DEFAULT = REATTACH + REDEFINE                     + UNDEFINED
    ALL     = REATTACH + REDEFINE + REPLACE_FORMATTER + UNDEFINED

The value of the ``warnings`` parameter of the ``LCD`` constructor is any
combination of the "constants" in the above table. This value is saved
as an ``LCD`` instance attribute, which is exposed by the read-write
``warnings`` property.

........ BLAH BLAH ........


REATTACH (corrected; default: reported)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`lcd` detects and eliminates duplicates in lists of handlers or filters
that are to be attached to higher-level entities. If ``REATTACH`` is turned on
in ``warnings``, `lcd` will report the duplicate (by printing a warning message
to stderr), indicating the source file and line number of the offending method
call.


REDEFINE (default: reported)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..... blah blah .....

``REPLACE_FORMATTER`` (default: not reported)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..... blah blah .....

``UNDEFINED`` (default: reported)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..... blah blah .....


.. _check:

Consistency checking — the ``check`` method
+++++++++++++++++++++++++++++++++++++++++++++++++

Called automatically in ``config()`` if the ``warnings`` property is ``0``.

What it does

    check for "undefined" things; if any exist, check reports
    all of them, and raises KeyError; otherwise, it returns ``self``).

<<<<<<< TODO >>>>>>>

