.. _overview:

Overview of Logging
=============================================

Logging is an important part of a program's internal operations, an essential
tool for development, debugging, troubleshooting, performance-tuning and
general maintenance. A program *logs messages* in order to record
its successive states, and to report any anomalies, unexpected situations or
errors, together with enough context to aid diagnosis. Messages can be logged
to multiple destinations at once — ``stderr`` in a terminal, a local file,
the system log, email, or a Unix log server over TCP, to cite common choices.

At the end of this chapter we provide several :ref:`logging_docs_links`,
for reference and general culture. It's not our purpose to rehash or
repeat the extensive (and generally quite good) documentation for Python's
`logging` package; in fact, we presuppose that you're familiar with basic
concepts and standard use cases. Nevertheless, it will be helpful to review
several topics.


Using `logging`
-------------------------------------

A program logs messages using the ``log`` method of objects called *loggers*,
which are implemented in `logging` by the ``Logger`` class. You can think of
the ``log`` method as a pumped-up ``print`` statement. It writes a message,
tagged with a level of severity, to one or more destinations.
In `logging`, a ``Handler`` object — a *handler* — represents a single
destination, together with a specified output format.
A handler implements abstract methods which format message data into structured
text and write or transmit that text to the output.
A logger contains zero or more handlers.
When a program logs a message by calling a logger's ``log`` method (or a
shorthand method such as ``debug`` or ``warning``), the logger dispatches the
message data to its handlers.

All messages have a `logging level`, or `loglevel`, indicating their severity
or importance. The predefined levels in ``logging`` are ``DEBUG``, ``INFO``,
``WARNING``, ``ERROR``, ``CRITICAL``, listed in order of increasing severity.
Both loggers and handlers have an associated *loglevel*, indicating a
severity threshold: a logger or a handler will filter out any message whose
loglevel is less than its own. In order for a message to actually be written
to a particular destination, its loglevel must equal or exceed the loglevels
of both the logger and the handler representing the destination.

This allows developers to dial in different amounts of logging verbosity:
you might set a logger's level to ``DEBUG`` in development but to
``ERROR`` in production. There's no need to delete or comment out
the lines of code that log messages, or to precede each such block with a
conditional guard. The logging facility is a very sophisticated version
of using the `print` statement for debugging.


`logging` classes that can be configured
-----------------------------------------------

`logging` defines a few types of entities, culminating in the ``Logger``
class. In general, a program or library will set up, or *configure*, logging
only once, at startup. This entails specifying message formats, destinations,
loggers, and containment relations between those things. Once a program has
configured logging as desired, use of loggers is very straightforward.
Configuration, then, is the only barrier to entry.

The following diagram displays the types that can be configured statically,
and their dependencies:

.. index:: diagram: The objects of `logging` configuration

.. _logging-config-classes:

.. figure:: logging_classes_v2.png

    The objects of `logging` configuration

    +-----------------------+-----------------------+
    | Symbol                | Meaning               |
    +=======================+=======================+
    | .. image:: arrowO.png | has zero or more      |
    +-----------------------+-----------------------+
    | m: 0/1                | many-to-(zero-or-one) |
    +-----------------------+-----------------------+
    | m: n                  | many-to-many          |
    +-----------------------+-----------------------+


In words:

    * a ``Logger`` can have one or more ``Handler``\s, and a ``Handler``
      can be used by multiple ``Logger``\s;
    * a ``Handler`` has at most one ``Formatter``, but a ``Formatter``
      can be shared by multiple ``Handler``\s;
    * ``Handler``\s and ``Logger``\s can each have zero or more ``Filter``\s;
      a ``Filter`` can be used by multiple ``Handler``\s and/or ``Logger``\s.


What these objects do
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A ``Formatter`` is basically just a format string that uses keywords
defined by the `logging` module — for example, ``'%(message)s'`` and
``'%(name)-20s: %(levelname)-8s: %(message)s'``.

A ``Handler`` formats and writes formatted logged messages to a particular
destination — a stream (e.g. ``sys.stderr``, ``sys.stdout``, or an in-memory
stream such as an ``io.StringIO()``), a file, a rotating set of files, a socket,
etc. A handler without a formatter behaves as if it had a ``'%(message)s'``
formatter.

A ``Logger`` sends logged messages to its associated handlers. Various
criteria filter out which messages are actually written, notably loglevel
thresholding as described above.

``Filter``\s provide still more fine-grained control over which messages are
written.

Loggers are identified by name
-------------------------------------------

A logger is uniquely identified by name: the expression
``logging.getLogger('mylogger')``, for example, always denotes the same object,
no matter where in a program it occurs or when it's evaluated.
The `logging` package always creates a special logger, the *root logger*, whose
name is ``''``; it's accessed by the expression ``logging.getLogger('')``,
or equivalently by ``logging.getLogger()``.

Logger names are *dotted names*, and behave in a way that's analogous to package
and module names. The analogy is intentional, to facilitate a style of logging
in which each package, and/or each module, uses its own logger, with names
``__package__`` and ``__name__`` respectively. The basic idioms are, for example::

    logging.getLogger(__name__).debug("About to do that thing")

and::

    logging.getLogger(__package__).warning("dict of defaults is empty")

A parent-child relation obtains among loggers: the parent of a logger ``a.b.c``
is the logger ``a.b``, whose parent is ``a``; the parent of logger ``a`` is the
root logger.

`logging` defaults
---------------------
`logging` supplies reasonable out-of-the-box defaults and shorthands so that you
can easily start to use its capabilities.

When accessed for the first time, the ``Logger`` named ``'mylogger'`` is created
"just in time" if it hasn't been explicitly configured. You don't *have* to
attach handlers to ``'mylogger'``; logging a message with that logger will "just
work". If ``'mylogger'`` has no handlers and you say:

    ``logging.getLogger('mylogger').warning("Hi there")``

then ``Hi there`` will be written to ``stderr``. Here's why: by default, a
logger "propagates" messages to its parent, so if ``'mylogger'`` lacks
handlers, the message will be logged by its parent, using the parent's handlers.
The parent of ``'mylogger'`` is the root, which by default (in the absence of
configured handlers) writes messages to ``stderr``.

The ``debug(...)`` logger method shown above is a shorthand for
``log(logging.DEBUG, ...)``. Similarly, there are convenience methods ``debug``,
``info``, ``error`` and ``critical``.

For another example, you can just say:

    ``logging.error("Something went wrong")``

and something plausible will happen (again, the string will be written to
``stderr``). This works because ``logging.error(...)`` is a shorthand for
``logging.log(logging.ERROR, ...)``, which in turn is a shorthand for
``logging.getLogger().log(logging.ERROR, ...)``.

In many cases, to configure logging it's sufficient just to add a handler or
two and attach them to the root.

    The `logging.basicConfig() <https://docs.python.org/3/library/logging.html#logging.basicConfig>`_
    function lets you configure the root logger, anyway to a point, using
    a monolithic function that's somewhat complex yet of limited capabilities.

--------------------------------------------------------

In the next chapter, we'll examine the approaches to configuration offered by
`logging`, and then see how `prelogging` simplifies the process.

--------------------------------------------------------

.. _logging_docs_links:

`logging` documentation links
----------------------------------------------------

See the `logging docs <https://docs.python.org/3/library/logging.html?highlight=logging>`_
for the official explanation of how Python logging works.

For the definitive account of static configuration, see the documentation of
`logging.config <https://docs.python.org/3/library/logging.config.html?highlight=logging>`_,
in particular the documentation for
`the format of a logging configuration dictionary <https://docs.python.org/3/library/logging.config.html#logging-config-dictschema>`_.

Here's a useful reference:
`the complete list of keywords that can appear in formatters <https://docs.python.org/3/library/logging.html?highlight=logging#logrecord-attributes>`_.

The logging `HOWTO <https://docs.python.org/3/howto/logging.html>`_
contains tutorials that show typical setups and uses of logging, configured in
code at runtime.
The `logging Cookbook <https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook>`_
contains a wealth of techniques, several of which exceed the scope of `prelogging` because
they involve `logging` capabilities that can't be configured statically (e.g.
the use of
`LoggerAdapters <https://docs.python.org/3/library/logging.html#loggeradapter-objects>`_,
or
`QueueListeners <https://docs.python.org/3/library/logging.handlers.html?#queuelistener>`_
). A few of the examples contained in the `prelogging` distribution are examples from
the Cookbook and HOWTO, reworked to use `prelogging`.

The `logging` package supports multithreaded operation, but does **not** directly support
`logging to a single file from multiple processes <https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes>`_.
Happily, `prelogging` does, in a couple of ways.

One additional resource merits mention: the documentation for
`logging in Django <https://docs.djangoproject.com/en/1.9/topics/logging/>`_
provides another, excellent overview of logging and configuration, with
examples. Its first few sections aren't at all Django-specific.
