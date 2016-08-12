.. _overview:

Overview
===============

.. todo:: this section! (in progress)

Logging is an important part of a program's internal operations, an essential
tool for development, debugging, troubleshooting, performance-tuning and
general maintenance. A program will *log messages* in order to record
its successive states, and to report any any anomalies, unexpected situations or
errors, together with the context in which occurred. Messages can be logged
to multiple destinations at once — e.g. ``stderr`` in a terminal, a local file,
a Unix log server over TCP.

In `logging`, a ``Handler`` object represents a single destination,
together with a specified output format. A handler implements abstract
methods which format message data into structured text, and write
or transmit that text to the output.
.
When a program logs messages, it doesn't interact with handlers, but rather
with more general objects called `loggers`. A ``Logger`` contains zero or more
handlers. When a program calls a logger's ``log`` method, the logger dispatches
the message data (including the string) to its handlers.

All messages have a `level` or `loglevel`, indicating their severity or importance
— `debug`, `info`, `warning`, `error`, `critical` are the basic categories.
Both loggers and handlers have an associated *loglevel*, indicating a severity
threshold: a logger or a handler will filter out (squelch) any message whose
loglevel is less than its own. In order for a message to actually be written
to a particular destination, its loglevel must equal or exceed the loglevels
of both the logger and the handler representing the destination.

This allows developers to dial in different amounts of logging verbosity:
you might set a logger's level to ``DEBUG`` in development but to
``WARNING`` or ``ERROR`` in production. There's no need to delete or comment out
the lines of code that log messages, or to precede each block with a guard.
The logging facility is a very sophisticated version of using the `print`
statement for debugging.


Python's `logging` package is a very capable library, if imperfect.
The purpose of the package is to provide *loggers* — objects that a program
uses to conditionally write structured text *messages* to zero or more
destinations.

In general, a program will *configure* logging once, at startup, by specifying
message formats, destinations, loggers, and containment relations between
those things. Once a program has set up logging as desired, use of loggers
is very straightforward. Configuration, then, is the only barrier to entry.

`logging` provides two ways to configure logging: statically, with text or a dictionary;
or dynamically, with code that uses the `logging` API.

Configuring logging with code is arguably less flexible than doing so statically.
(statically, every logging entity is identified by name)
Benefits of dynamic configuration:

    * You can take advantage of the reasonable defaults provided by the methods
      of the `logging` API. When configuring logging statically, various fussy
      defaults must be specified explicitly.
    * You can configure the entities of logging (formatters, optional filters,
      handlers, loggers) one by one, in order, starting with those that don't
      depend on other entities, and proceeding to those that use entities
      already defined. All entities are identified by *name*.
    * It's easier to debug: each step taken is rather small, and you can fail
      faster than when configuring from an entire dictionary.

Deficiencies of dynamic configuration
    * Except for loggers, none of the entities you create have *names*,
      so you must use program variables (addresses of live objects) to
      refer to them — say, when attaching handlers to a logger.

    * Somehow it winds up more even verbose than static dictionaries —
      the methods are low-level, and many boilerplate passages recur
      in dynamic configuration code.

`lcd` occupies a middle ground: it provides a clean, consistent and concise
API for incrementally constructing dicts  configure logging
statically. The ``add_*`` methods let you specify new logging entities
entities (formatters, possibly filters, handlers, loggers), which all have names.
and ``attach_*``
update the dict with specifications of logging

`logging` shortcomings
    * API is at once complex and limited
    * with static config, no warnings or error checking until dictConfig (or fileConfig) called
    * awkward to extend
    * entire library written in thoroughgoing camelCase (inconsistent, at that)


`lcd` (for
**l**\ogging **c**\onfig **d**\ict) provides a streamlined API for setting up
logging, making it easy to use "advanced" features such as rotating log files.
`lcd` also supplies missing functionality: the package provides
multiprocessing-safe logging to the console, to files and rotating files, and
to `syslog`.

It's not our purpose to rehash or repeat the extensive (and generally quite
good) logging documentation; in fact, we presuppose that you're familiar with
basic concepts and standard use cases. At the end of this section we
provide :ref:`links_to_sections_of_logging_docs`.
Nevertheless, it will be helpful to review a few topics.


(( Worth mentioning that Django uses static configuration -- indicates importance of static logging. ))

`lcd` (for
**l**\ogging **c**\onfig **d**\ict) provides a streamlined API for setting up
logging statically. `lcd` makes it easy to use "advanced" features such as
rotating log files.

error-checking and warnings ! :)

inconsistent camelCase <-- fixups


----- Using LCD, you build a logging config dict using a flat succession of
method calls that all take keyword arguments. instead of a static declaration
of a triply nested dict and its excess of glyphs (curly braces, quotes,
colons). Each call to one of the ``add_*`` methods adds an item
to one of the subdictionaries ``'formatters'``, ``'filters'``, ``'handlers'``
or ``'loggers'``. You can specify all of the item's dependencies in this call,
using names of previously added items, and/or you can add dependencies
subsequently with the ``attach_*`` methods. For example, in the following code:

.. code::

    >>> from lcd import LCD
    >>> d = LCD()
    >>> d.add_formatter('simple', '{message}', style='{')

the ``add_formatter`` call adds an item to the ``'formatters'``
subdictionary of ``d``. If ``d`` were declared statically as a dict,
it would look like this::

    d = {
        # ...

        'formatters' : { # ...
                         'simple': { format: '{message}',
                                     'style': '{' },
                         # ...
                       },
        'handlers':    { # ...
                       },

        # ...
    }

An LCD makes its top-level subdictionaries available as properties with the
same names as the keys: d.formatters == d['formatters'], d.handlers == d['handlers'],
and similarly for d.filters, d.loggers, d.root. After the above ``add_formatter``
call, ::

    >>> d.formatters                # ignoring whitespace,
    {'simple': {format: '{message}',
                'style': '{'}
    }



Logging a message
-------------------

The `logging` module lets us log messages to various destinations, affording us
a lot of control over what actually gets written where, and when. We use
``Logger`` objects to log messages; ultimately, all the other types defined by
`logging` exist only to support this class.

A ``Logger`` is uniquely identified by name: the expression
``logging.getLogger('mylogger')``, for example, always denotes the same object,
no matter where in a program it occurs or when it's evaluated. When evaluated
for the first time, the ``Logger`` named ``'mylogger'`` is created
"just in time" if it hasn't been explicitly configured. You don't _have_ to
configure ``'mylogger'``; the expression accessing it will "just work", and
then, at least by default, that logger will use the handlers of it's
*parent handler*. The parent of ``'mylogger'`` is the
root logger, ``logging.getLogger()``

.. todo:: Discuss, here or previously, the parent-child relationship
    among/between loggers, induced by dotted logger names a la package names.
    (which makes package names well-suited for use as logger names).

    Might be worth mentioning in discussing complexities of `logging` — non-OOP
    inheritance (delegation to parent if no handlers), propagation

In many cases, to configure logging it's sufficient just to add a handler or
two and attach them to the root.

.. topic:: `logging` shorthands and defaults

    `logging` supplies reasonable out-of-the-box defaults so that you can easily
    start to use its capabilities. You can just say:

        ``logging.error("Something went wrong")``

    and something plausible will happen (the string will be written to
    ``stderr``). This statement is a shorthand that implicitly uses the "root
    logger", which the `logging` module always creates. By default, the root
    logger writes messages to ``stderr``. All loggers are identified uniquely
    by name; the root logger's name is  ``''``.

    .. todo:: The parent-child relationship among/between loggers, induced by their names;
        There's a kind of "inheritance", though in the style of event handlers not OOP.
        Complexity: by default, a logger delegates to its parent, but it also has a separate
        'propagate' setting governing blah-blah

    The `logging.basicConfig() <https://docs.python.org/3/library/logging.html#logging.basicConfig>`_
    function lets you configure the root logger, anyway to a point, using
    a monolithic function that's somewhat complex yet of limited capabilities.

    .. todo::
        The above subsection is a ".. topic::".
        Does it work? does this material belong here,
        is its relevance to the foregoing clear?


`logging`-configuration classes
----------------------------------

There are just a few types of entities involved in the configuration of logging.
These classes are all defined in the `logging` module. The following diagram
displays them and their dependencies:

.. figure:: logging_classes.png

    The objects of `logging` configuration

    +-----------------------+-----------------------+
    | Symbol                | Meaning               |
    +=======================+=======================+
    | .. image:: arrow.png  | has one or more       |
    +-----------------------+-----------------------+
    | .. image:: arrowO.png | has zero or more      |
    +-----------------------+-----------------------+
    | m: 1                  | many-to-one           |
    +-----------------------+-----------------------+
    | m: n                  | many-to-many          |
    +-----------------------+-----------------------+


In words:
    * a ``Logger`` can have one or more ``Handler``\s, and a ``Handler``
      can be used by multiple ``Logger``\s;
    * a ``Handler`` has just one ``Formatter``, but a ``Formatter``
      can be shared by multiple ``Handler``\s;
    * ``Handler``\s and ``Logger``\s can each have zero or more ``Filter``\s.


Review of what these objects do
+++++++++++++++++++++++++++++++++

A ``Formatter`` is basically just a format string that uses keywords
defined by the `logging` module — for example, ``'%(message)s'`` and
``'%(name)-20s: %(levelname)-8s: %(message)s'``.

A ``Handler`` writes formatted logged messages to a particular destination —
a stream (e.g. ``sys.stderr``, ``sys.stdout``, or an in-memory stream such as an
``io.StringIO()``), a file, a rotating set of files, a socket, etc.

A ``Logger`` sends logged messages to its associated handlers. Various
criteria filter out which messages are actually written.

Every message that a logger logs has a *level* — a *loglevel*, as we'll call it:
an integer indicating the severity of the message. The standard levels defined
by the `logging` module are, in order of increasing severity and numeric value:
``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, and ``CRITICAL``.
Every logger has
corresponding methods (``debug()``, ``info()`` and so on) for emitting messages
at the named loglevel. Each of these methods is just a shorthand for calls to
the ``log`` method at a fixed loglevel. For example, you might log a ``WARNING``
message ``"Be careful!"`` to the logger named ``'mylogger'`` with the statements

.. code:

    logger = logging.getLogger('mylogger')
    logger.warning("Be careful!")

The last statement is shorthand for ``logger.log(logging.WARNING, "Be careful!")``.

Every ``Handler`` and every ``Logger`` has a threshold loglevel.

The loglevel of a message must equal or exceed the loglevel of a logger in
order for the logger to send the message to its handlers. In turn, a handler
will write a message only if the message's loglevel also equals or exceeds
that of the handler.

``Filter``\s provide still more fine-grained control over which messages are
written.


Order of definition
+++++++++++++++++++++++++++++++++

While configuring logging, you give a name to each of the objects that you
define. When defining a higher-level object, you identify its constituent
lower-level objects by name.

``Formatter``\s and ``Filter``\s (if any) don't depend on any other logging
objects, so they should be defined first. Next, define ``Handler``\s, and
finally, ``Logger``\s that use already-defined ``Handler``\s (and, perhaps,
``Filter``\s). `lcd` supplies dedicated methods for configuring the root logger
(setting its level, attaching handlers and filters to it), but often a
general-purpose `lcd` method can also be used, by referring to the root logger
by name: ``''``.

.. note::
    Once logging is configured, only the names of ``Logger``\s persist.
    `logging` retains *no associations* between the names you used to specify
    ``Formatter``, ``Handler`` and ``Filter`` objects, and the objects
    constructed to your specifications; you can't access those objects by any
    name.

Typically, we won't require any ``Filter``\s, and then, setting up logging
involves just these steps:

* define ``Formatter``\s
* define ``Handler``\s that use the ``Formatter``\s
* define ``Logger``\s that use the ``Handler``\s.

In common cases, such as the :ref:`example-overview-config` of the next section,
`lcd` eliminates the first step and makes the last step trivial.


Configuring `logging` statically
-----------------------------------

The `logging.config` submodule offers two equivalent ways to specify
configuration statically:

* with a dictionary meeting various requirements, which is
  passed to ``logging.config.dictConfig()``;
* with a text file written in YAML, conforming to analogous requirements,
  and passed to ``logging.config.fileConfig()``.

The `schema for configuration dictionaries <https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema>`_
documents the format of such dictionaries — and uses YAML to do so!, to cut down
on the clutter of quotation marks and curly braces. Arguably, this documentation
makes it seem quite daunting to configure logging with a ``dict``. Following its
precepts, you must create a medium-sized ``dict`` containing several nested
``dict``\s, in which many values refer back to keys in other sub\``dict``\s —
a thicket of curly braces, quotes and colons, which you finally pass to
``dictConfig()``.

`lcd` defines two classes, a ``dict`` subclass ``LCD``, and `its` subclass
``LCDEx``, which represent logging configuration dictionaries — *logging config
dicts*, for short. ``LCD`` provides the basic model of building a logging config
dict; ``LCDEx`` supplies additional conveniences including predefined formatters
and easy access to [*???????*] "advanced" features such as multiprocessing-safe
rotating file handlers.

You use the methods of these classes to add specifications of named
``Formatter``\s, ``Handler``\s, ``Logger``\s, and optional ``Filter``\s, and
containment relations between them. Once you've done so, calling the
``config()`` method of a ``LCD`` configures logging by passing itself, as a
``dict``, to ``logging.config.dictConfig()``. This call creates all the objects
and linkages specified by the underlying dictionary.


.. _example-overview-config:

Example
++++++++

Suppose we want the following logging configuration:

    Messages should be logged to both ``stderr`` and a file. Only messages with
    loglevel ``INFO`` or higher should appear on-screen, but all messages should
    be logged to the file. Messages to ``stderr`` should consist of just the
    message, but messages written to the file should contain the logger name and
    the message's loglevel.

This suggests two handlers, each with an appropriate formatter — a ``stderr``
console handler with level ``INFO``, and a file handler with level ``DEBUG``.
Both handlers should be attached to the root logger, which must have level
``DEBUG`` (or ``NOTSET``) to allow all messages through.

Once this configuration is established, these logging calls:

.. code::

    import logging
    root_logger = logging.getLogger()
    root_logger.debug("1. 0 = 0")
    root_logger.info("2. days are getting shorter")
    root_logger.debug("3. 0 != 1")
    # ...
    logging.getLogger('submodule_A').info("4. submodule_A initialized")

should produce the following ``stderr`` output:

.. code::

    2. days are getting shorter
    4. submodule_A initialized

and the logfile should contain (something much like) these lines:

.. code::

    root                : DEBUG   : 1. 0 = 0
    root                : INFO    : 2. days are getting shorter
    root                : DEBUG   : 3. 0 != 1
    submodule_A         : INFO    : 4. submodule_A initialized


Let's see what it's like to set this up — with `lcd`, and without it.

Configuration with `lcd`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`lcd` simplifies the creation of "logging config dicts" by breaking the process
down into easy, natural steps. As much as is possible, with `lcd` you only have
to specify the objects you care about and what's special about them; everything
else receives reasonable, expected defaults. Using the "batteries included"
``lcd.LCDEx`` class lets us concisely specify the desired setup:

.. code::

    from lcd import LCDEx

    lcd_ex = LCDEx(root_level='DEBUG',
                   attach_handlers_to_root=True)
    lcd_ex.add_stderr_handler(
                    'console',
                    formatter='minimal',
                    level='INFO'
    ).add_file_handler('file_handler',
                       formatter='logger_level_msg',
                       filename='blather.log',
    )
    lcd_ex.config()

Here, we use a couple of the builtin ``Formatter``\s supplied by
``LCDEx``. Because we pass the flag
``attach_handlers_to_root=True`` when creating the instance ``lcd_ex``,
every handler we add to ``lcd_ex`` is automatically attached to the root logger.
Later, we'll
:ref:`revisit this example <overview-example-using-only-LCD>`,
to see how to achieve the same result using only ``LCD``.

Remarks
^^^^^^^^^^

To allow chaining, as in the above example, the methods of ``LCD``
and ``LCDEx`` generally return ``self``.

You can use the ``dump()`` method of a ``LCD`` to prettyprint its
underlying ``dict``. In fact, that's how we determined the value of
``config_dict`` for the following subsection.


Configuration without `lcd`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Without `lcd`, you could configure logging to satisfy the stated requirements
using code like this:

.. code::

    import logging

    config_dict = \
        {'disable_existing_loggers': False,
         'filters': {},
         'formatters': {'logger_level_msg': {'class': 'logging.Formatter',
                                             'format': '%(name)-20s: %(levelname)-8s: '
                                                       '%(message)s'},
                        'minimal': {'class': 'logging.Formatter',
                                    'format': '%(message)s'}},
         'handlers': {'console': {'class': 'logging.StreamHandler',
                                  'formatter': 'minimal',
                                  'level': 'INFO'},
                      'file_handler': {'class': 'logging.FileHandler',
                                       'delay': False,
                                       'filename': 'blather.log',
                                       'formatter': 'logger_level_msg',
                                       'level': 'DEBUG',
                                       'mode': 'w'}},
         'incremental': False,
         'loggers': {},
         'root': {'handlers': ['console', 'file_handler'], 'level': 'DEBUG'},
         'version': 1}

    logging.config.dictConfig(config_dict)


.. _links_to_sections_of_logging_docs:

Links to sections of the `logging` documentation
----------------------------------------------------

See the `logging docs <https://docs.python.org/3/library/logging.html?highlight=logging>`_
for the official explanation of how logging works.

For the definitive account of static configuration, see the documentation of
`logging.config <https://docs.python.org/3/library/logging.config.html?highlight=logging>`_.

The logging `HOWTO <https://docs.python.org/3/howto/logging.html>`_
contains tutorials that show typical setups and uses of logging, configured in
code at runtime.
The `logging Cookbook <https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook>`_
contains a wealth of techniques, several of which exceed the scope of `lcd` because
they involve `logging` capabilities that can't be configured statically (e.g.
the use of
`LoggerAdapters <https://docs.python.org/3/library/logging.html#loggeradapter-objects>`_,
or
`QueueListeners <https://docs.python.org/3/library/logging.handlers.html?#queuelistener>`_
).

The `logging` package supports multithreaded operation, but does **not** support
`logging to a single file from multiple processes <https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes>`_.
Happily, `lcd` does, in a couple of ways.


