.. include:: ../docs/_global.rst

README for `prelogging` 0.4.1
=================================

See the full documentation at `https://prelogging.readthedocs.io <https://prelogging.readthedocs.io/>`_.

`prelogging` streamlines the process of *configuring* logging in Python, as provided by the
`logging <https://docs.python.org/3/library/logging.html?highlight=logging#module-logging>`_
package in the Python standard library. It presents a straightforward, consistent API for
specifying how you want logging set up — the format of messages, their destinations
and loglevels (severity thresholds), and so on. While `prelogging` aims at clarity
and simplicity, it in no way prevents you from using any of `logging`'s features.
It's intended for experts and novices alike.

A program *logs messages* in order
to record its successive states, and to report any anomalies, unexpected situations
or errors, together with enough context to aid understanding and diagnosis. Messages
can be logged to multiple destinations at once — ``stderr`` in a terminal, a local file,
the system log, email, or a Unix log server over TCP, to cite common choices.
Logging is a very sophisticated version of using the ``print`` statement for debugging.

Once you've configured logging, using it is easy and powerful. Configuration, then,
is the barrier to entry.

`prelogging` attempts to help you set up logging to give the results you hope for: messages
appearing in the formats you want, where you want, when you want (that is, at what times,
or under what conditions). `prelogging` makes some of the more advanced capabilities
of `logging` easily accessible. It even supplies missing functionality: it provides
multiprocessing-safe logging to the console, files, rotating files, and `syslog`.

When logging is correctly set up to your liking, the benefits can be great. When
you or a colleague examines a log file, you can more quickly find the information
you seek, because each message was written to the place you expect (just once!),
under just the circumstances you intended, and in the format you're looking for.

Getting configuration right, however, can be tricky. Infrequent
or novice users of the `logging` package can despair of messages written
multiple times to the same or different destinations, to unintended
destinations, not when expected, or even not at all. `logging` is a respectably
powerful and complex package whose basic ways of doing things may not be quickly
apparent. Understanding how `logging` works is essential to getting the most out
it. `prelogging`'s documentation and examples can help clarify much about `logging`
that may seem murky.

Using prelogging
-------------------------

With `prelogging`, you construct a *logging configuration dictionary*, or
*logging config dict*, a dict in the format expected by `logging`'s
``dictConfig()`` function. (We'll behold one below.)

Logging config dicts are represented in `prelogging` by the ``LCDict`` class. You call
the methods of this class on an instance to incrementally build a logging config dict,
adding specifications of formatters, filters (if any), handlers, and loggers other
than the root if you want any. When adding these descriptions of logging entities,
you give them names, and then refer to them by those names in subsequent method calls –
for example, when attaching an already-described formatter to a handler, or attaching
already-described handlers to a logger.

When you've added all the elements you require, a call to the instance's ``config()``
method results in a call to ``logging.config.dictConfig()``, which configures logging.
At this point, you are most likely done with the ``LCDict`` instance. You access
loggers with the ``logging.getLogger(name)`` function, as usual, using the ``name``\s
you gave them.

.. sidebar:: is-a or has-a

    The ``LCDict`` class, which represents logging config dicts, is a subclass of ``dict`` –
    It doesn't *contain* a dict, it *is* one. In ordinary and intended uses, this can be
    considered an implementation detail: the methods of ``"LCDict`` are sufficient to build
    a logging config dict, without any calls to ``dict`` methods. Nevertheless, you really
    *are* building a ``dict``, after all, and it would be premature and presumptuous to
    offer a nanny-API which denies that.

Requirements
---------------

The `prelogging` package requires only Python 3.4+ or 2.7. It has no external
dependencies.

Very little of `prelogging`\'s code is sensitive to Python 3 vs 2.
To address the few remaining differences, we've used `six`, sparingly (one decorator,
one function, and one constant). The `prelogging` package includes a copy of the
``six.py`` module (presently v1.10.0, for what it's worth), so no separate
installation is required.

Installation
---------------

You can install `prelogging` from PyPI (the Python Package Index) using ``pip``::

    $ pip install prelogging

(Here and elsewhere, ``$`` at the beginning of a line indicates your command
prompt, whatever that may be.)

Alternately, you can

* clone the github repo, or
* download a ``.zip`` or ``.tar.gz`` archive of the repository
  from github or PyPI, and uncompress it

to a fresh directory, change to that directory, and run::

    $ python setup.py install

Downloading and uncompressing the archive lets you review, run and/or copy the
tests and examples, which aren't installed by ``pip`` or ``setup.py``. Whichever
method you choose to install `prelogging`, ideally you'll do it in a `virtual
environment <https://docs.python.org/3/tutorial/venv.html>`_.

Tests and Examples
----------------------------

The `prelogging` repository contains the ``tests/`` and ``examples/`` subdirectories.

The tests are as thorough as is reasonable, and achieve from 88% to 100% coverage
depending on the module.

The examples illustrate many basic and advanced uses, including several adaptations
of examples in the `Logging HOWTO <https://docs.python.org/3/howto/logging.html>`_ guide
and `The Logging Cookbook <https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook>`_.
The `Guide to Examples <https://prelogging.readthedocs.io/en/latest/guide-to-examples.html>`_
in the full `prelogging` documentation catalogs all the examples and briefly
describes each one.

The tests and examples together achieve almost complete coverage.

-------------------------------------------------------------------------------

Quick Start
-------------------

.. uh ^^^ is next level heading char, to bump +++ down a level

In this section, we'll state some reasonable configuration requirements,
and examine three ways of configuring them with `prelogging` – a first attempt,
a more concise revision, and lastly a less concise version. These approaches
will let us compare the two ways that `logging` provides for achieving
the same configuration. Finally, we'll see how to leverage *ancestry* and *propagation*
among loggers so that the same configuration can cover more general situations than
first anticipated.


Basic Configuration Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's see how to configure logging with `prelogging`. Suppose we want the
following setup:

.. _example-overview-config:

    **Configuration requirements**

    Messages should be logged to both ``stderr`` and a file. Only messages with
    loglevel ``INFO`` or higher should appear on-screen, but all messages should
    be logged to the file. Messages to ``stderr`` should consist of just the
    message, but messages written to the file should also contain the logger
    name and the name of the message's loglevel.

    The logfile contents should persist: the file handler should *append*
    to the logfile, rather than overwriting it each time the program using these
    loggers is run.

This suggests two handlers, each with a distinct formatter and loglevel – a ``stderr``
stream handler with level ``INFO``, and a file handler with level ``NOTSET``.
(``NOTSET`` is the default loglevel for handlers. Numerically less than ``DEBUG``,
all loglevels are greater than or equal to it.)
Both handlers should be attached to the root logger, which should have level
``DEBUG`` to allow all messages through. The file handler should be created with
``mode='a'`` (append, not ``'w'`` for overwrite) so that the the logfile
contents can persist.

**Note**: Already these requirements exceed the abilities of ``logging.basicConfig()``
when used to configure logging in a single call. Used in that manner, the function
can create a stream handler or a file handler, but not both.

Using the example configuration
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Once this configuration is established, these logging calls:

.. code::

    import logging
    root_logger = logging.getLogger()
    # ...
    root_logger.debug("1. 0 = 0")
    root_logger.info("2. Couldn't create new Foo object")
    root_logger.debug("3. 0 != 1")
    root_logger.warning("4. Foo factory raised IndexError")

should produce the following ``stderr`` output – the messages with loglevel ``INFO``
or greater, with the simplest formatting:

.. code::

    2. Couldn't create new Foo object
    4. Foo factory raised IndexError

and the logfile should contain (something much like) these lines:

.. code::

    root                : DEBUG   : 1. 0 = 0
    root                : INFO    : 2. Couldn't create new Foo object
    root                : DEBUG   : 3. 0 != 1
    root                : WARNING : 4. Foo factory raised IndexError

Creating the example configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here's a first pass at using an ``LCDict`` to configure logging as required.
We've inserted two "debugging" statements (commented "FYI"), for your enlightenment.
After walking through this code, we'll look at a more concise version which takes
advantage of various conveniences offerred by ``LCDict``.

.. code::

    from prelogging import LCDict

    lcd = LCDict(root_level='DEBUG')
    print(isinstance(lcd, dict))    # FYI

    lcd.add_formatter('con', format='%(message)s')
    lcd.add_formatter('file', format='%(name)-20s: %(levelname)-8s: %(message)s')
    lcd.add_stderr_handler(
                    'h_stderr',
                    formatter='con',
                    level='INFO')
    lcd.add_file_handler('h_file',
                         formatter='file',
                         filename='blather.log')
    lcd.attach_root_handlers('h_stderr', 'h_file')  # attach handlers to root
    lcd.dump()                      # prettyprints the logging config dict (FYI)
    lcd.config()


This should remind you somewhat of how logging can be set up using the `logging` API.
However, most of these ``LCDict`` method calls accomplish more than the `logging` functions
and methods you'd use to create and relate logging entities with the same configuration
as this `prelogging` code achieves.
(Below, in the section :ref:`Creating the example configuration less concisely <mimicing_logging_API>`,
we'll mimic the `logging` API, to see that `prelogging` can be just as granular,
arguably to little good effect.)

First we create an ``LCDict``, which we call ``lcd`` — a logging config dict
with root loglevel ``'DEBUG'`` (the default root loglevel is ``'WARNING'``, as in `logging`).
The next line prints ``True``: an ``LCDict`` *is* a dict.

We add to it a couple of (descriptions of) formatters that the handlers will use,
naming them ``'con'`` and ``'file'``. Next, we add the handlers: first, one named
``'h_stderr'`` which writes to ``stderr``, uses the simpler format we named ``'con'``,
and has loglevel ``'INFO'``; second, a file handler ``'h_file'``, which writes to
a file ``'blather.log'`` (in the current directory), and has the default loglevel
``'NOTSET'``.. ``add_file_handler`` takes a ``mode`` keyword parameter, which
we didn't have to specify, as its default value is ``'a'`` (for *append*). The
last configuration step attaches the two handlers to the root logger.

Finally we configure logging by calling ``config()`` on ``lcd``, which basically
calls ``logging.config.dictConfig(self)`` to create all the specified entities
and relationships.

Just before ``config()``, we've called the ``dump()`` method to print the logging
config dict as a dict. ``lcd.dump()`` is basically a call to ``pprint.pprint(self)``
– ``LCDict`` doesn't override ``__str__`` or ``__repr__``. Here's what that line prints::

    {'disable_existing_loggers': False,
     'filters': {},
     'formatters': {'con': {'class': 'logging.Formatter', 'format': '%(message)s'},
                    'file': {'class': 'logging.Formatter',
                             'format': '%(name)-20s: %(levelname)-8s: %(message)s'}},
     'handlers': {'h_file': {'class': 'logging.FileHandler',
                             'delay': False,
                             'filename': 'blather.log',
                             'formatter': 'file',
                             'mode': 'a'},
                  'h_stderr': {'class': 'logging.StreamHandler',
                               'formatter': 'con',
                               'level': 'INFO',
                               'stream': 'ext://sys.stderr'}},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': ['h_stderr', 'h_file'], 'level': 'DEBUG'},
     'version': 1}

This is the dict that's passed to ``dictConfig()`` – a triply-nested thicket of
curly braces, quotes and colons. Typing or maintaining this, even with more
whitespace, seems unappealing. By contrast, `prelogging` lets you build this
dict entity by entity, omitting cruft and clutter.

**Note**: In `prelogging`, loglevels are always identified by their names
rather than their numeric values – thus, ``'DEBUG'`` not ``logging.DEBUG``, and
so on. The values of parameters to `prelogging` methods that change the logging
config dict generally become leaves of the nested dict, and they're mostly strings.

Creating the example configuration more concisely
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can simplify the code further::

    from prelogging import LCDict

    lcd = LCDict(root_level='DEBUG',
                 attach_handlers_to_root=True)
    lcd.add_stderr_handler(
                    'h_stderr',
                    formatter='msg',
                    level='INFO')
    lcd.add_file_handler(
                    'h_file',
                    formatter='logger_level_msg',
                    filename='blather.log')
    lcd.config()


Because handlers are so commonly attached to the root logger,
``LCDict`` makes it easy to do that.
In this shorter version, ``lcd`` is initialized with ``attach_handlers_to_root=True``.
As a result, the (specifications of the) two handlers are attached to the root
as soon as they're added to ``lcd``; it's no longer necessary to call
``lcd.add_root_handlers('h_stderr', 'h_file')``.
(``attach_handlers_to_root`` establishes a default for an ``LCDict``, which can
be overridden in any ``add_*_handler`` call with the keyword argument ``attach_to_root``.)

No formatters are explicitly created, yet the handlers reference formatters
named ``'msg'`` and ``'logger_level_msg'``. These are a couple of the `formatter
presets` supplied by `prelogging`. You can add your own formatter presets if
the rough dozen supplied don't suit your needs.

If we had called ``dump()`` on ``lcd`` just before ``config()``, we'd see a
dict identical to the one above except for the names of the formatters.

Chaining ``LCDict`` methods
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
The methods of ``LCDict`` (and of its superclass ``LCDictBasic``) that change
the state of the logging config dict all return ``self``, which makes chaining them
possible. We don't even need the ``lcd`` variable::

    LCDict(root_level='DEBUG',
           attach_handlers_to_root=True
    ).add_stderr_handler(
                    'h_stderr',
                    formatter='msg',
                    level='INFO'
    ).add_file_handler(
                    'h_file',
                    formatter='logger_level_msg',
                    filename='blather.log'
    ).config()


.. _mimicing_logging_API:

Creating the example configuration less concisely - mimicking the `logging` API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`prelogging` lets you make changes to the logging config dict with the same
granularity as the logging API requires. For illustration's sake, we'll write
our example in a *less* concise way. Here, each ``LCDict`` method does one small
thing at a time, corresponding 1-1 with the logging API calls you'd have to use
to actually construct the entities::

    lcd = LCDict()
    lcd.set_root_level('DEBUG')

    lcd.add_formatter('msg', format='%(message)s')
    lcd.add_formatter('logger_level_msg', format='%(name)-20s: %(levelname)-8s: %(message)s')

    lcd.add_stderr_handler('h_stderr')
    lcd.set_handler_formatter('h_stderr', 'msg')
    lcd.set_handler_level('h_stderr', 'INFO')

    lcd.add_file_handler('h_file', filename='blather.log')
    lcd.set_handler_formatter('h_file', 'logger_level_msg')
    lcd.set_handler_level('h_stderr', 'INFO')

    lcd.attach_root_handlers('h_stderr')
    lcd.attach_root_handlers('h_file')  # attach handlers to root

    lcd.config()

In `prelogging`, it's usually unnecessary to call the ``set_handler_formatter``
or ``set_*_level`` methods, and repeated consecutive calls to "attach" methods
can generally be coalesced into one call with a list parameter (or eliminated
altogether, by passing that list to a prior``add_*`` call).


Adding additional loggers that use the existing handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose you later add to your project a module ``new_module.py``, which will also
use logging, via its own logger ``'new_module'``. If it meets your needs for this
logger to use the existing handlers, then you can just *use it*,
no extra configuration required!

For example::

    # new_module.py
    import logging

    # ...
    # logging has already been configured -- handlers created & attached to root

    logger = logging.getLogger(__name__)    # __name__ == 'new_module'
    # ...
    logger.debug("It's 11:11 pm")
    logger.error("UH OH!")
    # ...

This writes the error message to ``stderr``::

    UH OH!!!!

and also appends both messages to the logfile, together with the logger name and level::

    new_module          : DEBUG   : It's 11:11 pm
    new_module          : ERROR   : UH OH!!!!

Why this works: ancestors and propagation
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. sidebar:: Ancestors and names

    The ancestor relation among loggers is, by default, the simple relation
    between their dotted names: L1 is an ancestor of L2 *iff* the name of L1 is a prefix
    of the name of L2, and no part between dots is split. The parent of a logger
    is its nearest ancestor. The root, whose name is ``''``, is an ancestor of every logger,
    and the parent of some. For example, a logger ``'foo'`` is ancestor of ``'foo.bar'``
    and ``'foo.bar.baz'``, but not of ``'foolserrand'``; ``'foo.bar'`` is an ancestor
    (the parent) of ``'foo.bar.baz'``, but not of ``'foo.bargeld'`` nor of
    ``'foo.bartend.sunday'``. Of the loggers just mentioned, only ``'foo'``
    has the root logger as parent.


A call to ``logging.getLogger`` creates the requested logger just in time, if it
doesn't already exist; all subsequent requests to get the logger of the same name
will return the same ``Logger`` object. Here, the name of the logger requested is
``'new_module'``, the value of ``__name__`` in this module. Like any newly created logger,
it has no handlers, its loglevel is ``'NOTSET'``, and logged messages *propagate*
to the handlers of its *ancestors* (``logger.propagate`` is ``True``).
The name of the root logger is simply ``''`` (empty string),
and it is the only ancestor of ``logger``. Thus, without any extra work,
all messages logged by ``logger`` will be sent directly to the root's handlers.

**Note**: If we attached a handler to this logger (during configuration, or after
configuration using the `logging` API), and if we left the logger's ``propagate``
flag set to True, then messages written by this logger would be sent to that handler
*as well as* to the two attached to the root.

-------------------------------------------------------------------------------

.. _supported-handlers:

Handler classes encapsulated by ``LCDict``
--------------------------------------------------

The `logging` package defines more than a dozen handler classes — subclasses of
``logging.Handler`` — in the modules ``logging`` and ``logging.handlers``.
``logging`` defines the basic stream, file and null handler classes, for which
``LCDictBasic`` supplies  ``add_*_handler`` methods. ``logging.handlers`` defines
more specialized handler classes, for about half of which (presently) ``LCDict``
provides corresponding ``add_*_handler`` methods.

.. index:: `'logging` handler classes encapsulated

.. _LCDict-handler-classes-encapsulated:

Handler classes that LCDict configures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

LCDict provides methods for configuring these `logging` handler classes, with
optional multiprocessing-aware "locking" support in most cases:

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

.. _auto-attach-handlers-to-root:

.. _easy-mp-safe-logging:

Easy multiprocessing-safe logging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As shown in the table above, `prelogging` provides multiprocessing-safe ("locking")
versions of the essential handler classes that write to the console, streams, files,
rotating files, and syslog.



--------------------------------------


Additional "batteries" included
----------------------------------------

.. _easy-filter-creation:
.. _filters:

Simplified creation and use of filters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Filters allow finer control than mere loglevel comparison over which messages
actually get logged. In conjunction with formatters, they can also be used
to add additional data fields to messages. Filters can be attached to handlers
and to loggers. In fact, the same filter can be attached to multiple handlers
and multiple loggers.

There are two kinds of filters: class filters and callable filters.
``LCDict`` provides a pair of convenience methods, ``add_class_filter`` and
``add_callable_filter``, which are easy to use – and much easier to use than
the lower-level ``LCDictBasic`` method ``add_filter``.

In Python 2, the `logging` module imposes a fussy requirement on callables
that can be used as filters, which the Python 3 implementation of `logging`
removes. The ``add_callable_filter`` method provides a single, sane interface
for adding callable filters that works in both Python versions.


.. _config-abc:

Configuration across modules and packages using ``LCDictBuilderABC``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One way for a larger program to configure logging is to pass around an
``LCDict`` to the different "areas" of the program, each contributing
specifications of its desired formatters, filters, handlers and loggers.
(Just what the "areas" of a program are, is in the eye of the developer. They
might be all modules, only certain major modules, all or some subpackages, etc.)

The ``LCDictBuilderABC`` class provides a mini-microframework that automates
this approach. Here, ``ABC`` stands for *abstract base class*. Each area of a
program only has to define an ``LCDictBuilderABC`` subclass and implement the
base class's abstract classmethod ``add_to_lcdict(lcd)``. Each implementation
contributes its specifications by calling methods on ``lcd``. These
implementations are *callbacks*: your code doesn't call them directly; rather,
they're called by ``LCDictBuilderABC.build_lcdict()``, which you *do* call.
``LCDictBuilderABC.build_lcdict`` *is* implemented and you shouldn't need to
override it.

Some presumably "top-level" area of the program calls the ``build_lcdict()``
classmethod of ``LCDictBuilderABC`` or a subclass, and that one call takes care
of the rest. ``build_lcdict()`` creates an ``LCDict`` – ``lcd``, say – using the
parameters passed to it, passes ``lcd`` to every ``add_to_lcdict()`` classmethod
of ``LCDictBuilderABC`` subclasses (roughly speaking), and returns ``lcd``.
Note that ``config()`` is *not* called in this process, to allow top-level
postprocessing of the returned ``LCDict``.

--------------------------------------

Next steps
------------
If you've made it this far, we're flattered, and grateful for your
interest in `prelogging`. You probably don't need encouragement to take it for
a spin, but ... please take it for a spin!

"Readme"s try to strike a balance between saying too little and saying too much.
This one probably falls off that tightrope a few times, erring in both ways.
For complete accounts of the topics introduced here,
solid explanations of how logging works,
and many useful techniques and recipes,
please check out `prelogging`'s actual `documentation <https://prelogging.readthedocs.io/>`_.

Happy logging!
