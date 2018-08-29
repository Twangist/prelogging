.. include:: ../docs/_global.rst

What it is, who it's for, why it is, what it does, why it's cool.

That function "logging.basicConfig" function (sic?) gets you set up with one call,
but it has complications and hard limitations: you can set up logging to the console,
or to a file, but not both; some parameters apply to only one of those situations.

----------

`prelogging` streamlines the process of *configuring* logging in Python, as provided by the
`logging <https://docs.python.org/3/library/logging.html?highlight=logging#module-logging>`_
package in the Python standard library. It presents a simple, streamlined, consistent API for
specifying how you want logging set up — the format of messages, their destinations
and loglevels (severity thresholds), and so on.

`prelogging` attempts to help you set up logging to achieve the results you want: messages
appearing in the formats you want, where you want, when you want (that is, at what times,
or under what conditions). `prelogging` makes some of the more advanced capabilities
of `logging` easilyl accessible. It even supplies missing functionality: it provides
multiprocessing-safe logging to the console, files, rotating files, and `syslog`.

When logging is correctly set up to your liking, the benefits can be great and
measurable. When you or a colleague examines a log file, you can more quickly
find the information you want, because each message was written to the place you
expect (just once!), under just the conditions you expected, and in the format you
expect.


`prelogging` offers a straightforward, consistent API for constructing a
*logging configuration dictionary*, or *logging config dict*, a dict in the format
expected by ``logging.dictConfig()``. At the same time, it in no way dumbs down
the very extensible and powerful `logging` API, nor does it prevent you from using
any of `logging`'s features.


Getting configuration right, however, can be tricky. Infrequent
or novice users of the `logging` package can despair of messages written
multiple times to the same or different destinations, to unintended
destinations, not when expected, or even not at all. `logging` is a respectably
powerful and complex package whose basic ways of doing things may not be quickly
apparent. Understanding how `logging` works is essential to getting the most out
it. The `prelogging` API


The logging package is very powerful,

>>>>>>>>>>> Next 2 paragraphs are more like, overview of using `prelogging``

Logging config dicts are represented in `prelogging` by the ``LCDict`` class. You call
the methods of this class on an instance to incrementally build a logging config dict,
adding specifications of formatters, filters (if any), handlers, and loggers other
than the root if you want any. When adding these descriptions of logging entities,
you give them names, and then refer to them by those names in subsequent method calls –
for example, when adding an already-described formatter to a handler, or adding
already-described handlers to a logger.

When you've added all the elements you require, a call to the instance's ``config()``
method results in a call to ``logging.dictConfig()``, which configures logging.
At this point, you are most likely done with the ``LCDict`` instance. Only the
names of loggers persist (and you access them with the ``logging.getLogger(name)``
function, using the names you gave them in the logging config dict); the `logging`
package doesn't retain the names of formatters or filters, and although it *does*
retain the names you gave to handlers, the read/write ``Handler`` property ``name``
remains undocumented in Python 3.7.



.. or: a note ????????
.. sidebar::

    The ``LCDict`` class, which represents logging config dicts, is a subclass of ``dict`` –
    It doesn't *contain* a dict, it *is* one. In ordinary and intended uses, this can be
    considered an implementation detail: the methods of ``"LCDict`` are sufficient to build
    a logging config dict, without any calls to ``dict`` methods. Nevertheless, you really
    *are* building a ``dict``, after all, and it would be premature and presumptuous to
    offer a nanny-API that prohibits you from doing whatever you might want to with that
    ``dict`` by tucking it away in a "private" data member.



README for `prelogging` |release|
=================================

See the full documentation at `https://pythonhosted.org/prelogging/ <https://pythonhosted.org/prelogging/>`_.

What `prelogging` is and does
------------------------------------------------

`prelogging` streamlines the process of *configuring* logging in Python, as provided by the
`logging <https://docs.python.org/3/library/logging.html?highlight=logging#module-logging>`_
package in the Python standard library. It presents a simple, consistent API for
speficying how you want logging set up — the format of messages, their destinations
and loglevels (severity thresholds), and so on. You can use it to configure logging
once and for all at startup, as well as to add additional logging entities.

Logging is an essential tool for development, debugging, troubleshooting,
performance-tuning and general maintenance. A program *logs messages* in order
to record its successive states, and to report any anomalies, unexpected situations
or errors, together with enough context to aid understanding and diagnosis. Messages
can be logged to multiple destinations at once — ``stderr`` in a terminal, a local file,
the system log, email, or a Unix log server over TCP, to cite common choices.
Logging is a very sophisticated version of using the `print` statement for debugging.

You *configure logging* by specifying message formats, destinations,
loggers (objects that log messages), and relationships between those things.
Once you've done so, use of loggers is straightforward and powerful.
Configuration, then, is the only barrier to entry.

The `logging` package provides a couple of approaches to configuration — static
(or declarative), using a dict or an analogous YAML text file; and dynamic (or
procedural), using the `logging` API. Both have their virtues and shortcomings.

`prelogging` offers a hybrid approach: a streamlined, consistent API for
incrementally constructing a *logging config dict* – a dict used to configure
logging, ultimately passed to ``logging.config.dictConfig()``. It's a thin,
extensible wrapper around the configuration capabilities of the `logging`
package.

In `prelogging`, you create an ``LCDict``, an object of a ``dict`` subclass representing
a logging config dict. You use the methods of this class to add each logging
entity and its dependencies (other, previously added logging entities) one by one,
instead of entering a single large thicket of triply-nested dicts. As you build
the configuration dict, by default `prelogging` checks for possible mistakes, and
issues warnings on encountering them.

`prelogging` also supplies missing functionality: it provides multiprocessing-safe
logging to the console, files, rotating files, and `syslog`.

For more information about `logging`, see the
`Overview of Logging <https://pythonhosted.org/prelogging/overview-of-logging.html>`_
chapter in the full documentation. Its last section provides several links to
`logging documentation, other overviews, and how-to's
<https://pythonhosted.org/prelogging/overview-of-logging.html#logging-documentation-links>`_.


Requirements
---------------

The `prelogging` package requires only Python 3.4+ or 2.7. It has no external
dependencies.

Very little of `prelogging`\'s code is sensitive to Python 3 vs 2.
To address the few remaining differences, we've used `six`, sparingly (one decorator,
one function, and one constant). The `prelogging` package includes a copy of the
``six.py`` module (v1.10.0, for what it's worth), so no separate installation is required.

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
environment <https://docs.python.org/3/tutorial/venv.html?highlight=virtual>`_.


Running tests and examples
----------------------------

The `prelogging` repository has a subdirectory `examples/` illustrating many
basic and advanced uses, including adaptations of examples in
the `logging HOWTO <https://docs.python.org/3/howto/logging.html>`_ guide
and the `logging Cookbook <https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook>`_.

.. sidebar:: All these scripts are executable on \*nix

    On Unix systems, including macOS, ``setup.py``, the ``run_*.py`` scripts
    and the examples are all executable and have proper
    `shebang <https://en.wikipedia.org/wiki/Shebang_(Unix)>`_\s, so for example
    you can use the command ``./root_logger.py`` instead of
    ``python root_logger.py``.


The top-level directory of the `prelogging` repository contains three scripts —
``run_tests.py``, ``run_examples.py`` and ``run_all.py`` — which let you run
all tests, all examples, or both, from the top-level directory. You can run
these before installing `prelogging`.

To run individual examples, first change into their subdirectory::

    $ cd examples/
    $ python root_logger.py     # or just ./root_logger.py

The `Guide to Examples <https://pythonhosted.org/prelogging/guide-to-examples.html>`_
in the full documentation catalogs all the examples and briefly
describes each one.

Coverage from tests + examples
+++++++++++++++++++++++++++++++++++

A few short passages, mostly Python-major-version-specific code, keep `prelogging`
shy of 100% coverage when both tests and examples are run:

+----------------------------+--------+-------+
|| Module                    || Py 3  || Py 2 |
+============================+========+=======+
|| ``lcdictbasic.py``        || \99%  || 100% |
|| ``lcdict.py``             || \98%  || \96% |
|| ``locking_handlers.py``   || 100%  || 100% |
|| ``lcdict_builder_abc.py`` || 100%  || 100% |
+----------------------------+--------+-------+

-------------------------------------------------------------------------------

Quick Start
-------------------

Suppose we want the following configuration:

.. _example-overview-config:

    **Configuration requirements**

    Messages should be logged to both ``stderr`` and a file. Only messages with
    loglevel ``INFO`` or higher should appear on-screen, but all messages should
    be logged to the file. Messages to ``stderr`` should consist of just the
    message, but messages written to the file should also contain the logger
    name and the message's loglevel.

    The logfile contents should persist: the file handler should **append**
    to the logfile, rather than overwriting it each time the program using these
    loggers is run.

This suggests two handlers, each with an appropriate formatter — a ``stderr``
stream handler with level ``INFO``, and a file handler with level ``NOTSET``.
(``NOTSET`` is the default loglevel for handlers. Numerically less than ``DEBUG``,
all loglevels are greater than or equal to it.)
Both handlers should be attached to the root logger, which should have level
``DEBUG`` to allow all messages through. The file handler should be created with
``mode='a'`` (append, not ``'w'`` for overwrite) so that the the logfile
contents can persist.

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
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Here's how we can use ``LCDict`` to configure logging to satisfy the above
:ref:`Configuration requirements <example-overview-config>`::

    from prelogging import LCDict

    lcd = LCDict(root_level='DEBUG',
                 attach_handlers_to_root=True)
    lcd.add_stderr_handler(
                    'h_stderr',
                    formatter='msg',    # actually not needed
                    level='INFO'
    ).add_file_handler('h_file',
                       formatter='logger_level_msg',
                       filename='blather.log',
    )
    lcd.config()

First we create an ``LCDict``, which we call ``lcd`` — a logging config dict
with root loglevel ``'DEBUG'``. An ``LCDict`` has a few attributes that aren't
part of the underlying dict, including the ``attach_handlers_to_root`` flag,
which we set to ``True``. The ``add_*_handler`` methods do just what you'd
expect: each adds a subdictionary to ``lcd['handlers']`` with the respective
keys ``'h_stderr'`` and ``'h_file'``, and with key/value pairs given by the
keyword parameters. Because lcd was initialized with ``attach_handlers_to_root=True``,
the two handlers were attached to the root logger upon creation; it wasn't
necessary to call ``lcd.add_root_handlers('h_stderr', 'h_file')``.

We've used a couple of the `Formatter presets` supplied by ``LCDict`` —
``'msg'`` and ``'logger_level_msg'``. Because we pass the flag
``attach_handlers_to_root=True`` when creating ``lcd``, every
handler we add to ``lcd`` is (by default) automatically
attached to the root logger. (You can override this default by passing
``add_to_root=False`` to any ``add_*_handler`` call.)

**Notes**

* To allow chaining, as in the above example, the methods of
  ``LCDict`` and its superclass ``LCDictBasic`` generally return ``self``.

* ``add_file_handler`` takes a ``mode`` keyword parameter, which we didn't have
  to specify, as its default value is ``'a'``.

* Here's the :ref:`complete table of prelogging's formatter presets <preset-formatters>`.


Adding additional loggers that use the existing handlers
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Suppose you later add to your project a module ``new_module.py``, which will also
use logging, via its own logger ``'new_module'``. If it meets your needs for this
logger to use the existing handlers, then you can just use this logger,
no extra configuration required!

For example::

    # new_module.py
    import logging

    logger = logging.getLogger(__name__)
    # ...
    logger.debug("It's 11:11 pm")
    logger.error("UH OH!")
    # ...

This writes the error message to ``stderr``::

    UH OH!!!!

and also appends both messages to the file, together with the logger name and level::

    new_module          : DEBUG   : It's 11:11 pm
    new_module          : ERROR   : UH OH!!!!

.. sidebar:: Ancestors and descendants

    The ancestor relation among loggers is the simple relation
    between their dotted names: L1 is an ancestor of L2 *iff* the name of L1 is a prefix
    of the name of L2, and no part between dots is split.
    For example, a logger ``foo`` is ancestor of ``foo.bar`` and ``foo.bar.baz``,
    but not of ``foolserrand``; ``foo.bar`` is an ancestor (the parent) of ``foo.bar.baz``,
    but not of ``foo.bargeld`` nor of ``foo.bartend.sunday``.

A call to ``logging.getLogger`` creates the requested logger just in time, if it
doesn't already exist; all subsequent requests to get the logger of the same name
will return the same ``Logger`` object. Here, the name of the logger requested is
'new_module', the value of ``__name__`` in this module. Like any newly created logger,
it has no handlers, its loglevel is ``'NOTSET'``, and logged messages *propagate*
to the handlers of its *ancestors* (``logger.propagate`` is ``True``).
The name of the root logger is simply ``''`` (empty string),
and it is the only ancestor of ``logger``. Thus, without any extra work,
all messages logged by ``logger`` will be sent directly to the root's handlers.

|br|

-------------------------------------------------------------------------------


`logging` classes that can be configured
--------------------------------------------------------

.. todo:: lead-in


`logging` defines a few types of entities, culminating in the ``Logger``
class. To configure logging is to specify message formats (formatters),
destinations (handlers), filters if any, loggers, and containment relations
between those things.

The following diagram displays the four types that can be configured statically,
and their dependencies:

.. index:: diagram: The objects of `logging` configuration

.. _logging-config-classes:

.. figure:: ../docs/logging_classes_v2.png

    The objects of `logging` configuration

    +-------------------------------+-----------------------+
    | Symbol                        | Meaning               |
    +===============================+=======================+
    | .. image:: ../docs/arrowO.png | has zero or more      |
    +-------------------------------+-----------------------+
    | m: 0/1                        | many-to-(zero-or-one) |
    +-------------------------------+-----------------------+
    | m: n                          | many-to-many          |
    +-------------------------------+-----------------------+


In words:

    * a ``Logger`` can have one or more ``Handler``\s, and a ``Handler``
      can be used by multiple ``Logger``\s;
    * a ``Handler`` has at most one ``Formatter``, but a ``Formatter``
      can be shared by multiple ``Handler``\s;
    * ``Handler``\s and ``Logger``\s can each have zero or more ``Filter``\s;
      a ``Filter`` can be used by multiple ``Handler``\s and/or ``Logger``\s.


What these objects do
+++++++++++++++++++++++++++++++

.. sidebar:: Keywords that can appear in formatters

    Here's
    `the complete list of them <https://docs.python.org/3/library/logging.html?highlight=logging#logrecord-attributes>`_.

A ``Formatter`` is basically just a format string that uses keywords
defined by the `logging` module — for example, ``'%(message)s'`` and
``'%(name)-20s: %(levelname)-8s: %(message)s'``.

A ``Handler`` formats and writes logged messages to a particular
destination — a stream (e.g. ``sys.stderr``, ``sys.stdout``, or an in-memory
stream such as an ``io.StringIO()``), a file, a rotating set of files, a socket,
etc. A handler without a formatter behaves as if it had a ``'%(message)s'``
formatter.

A ``Logger`` sends logged messages to its associated handlers. Various
criteria filter out which messages are actually written, notably loglevel
thresholding.

``Filter``\s provide still more fine-grained control over which messages are
written.

`prelogging`'s role
+++++++++++++++++++++++++++++++++++++++++

`prelogging` defines two classes which represent logging config dicts:
a ``dict`` subclass ``LCDictBasic``, and `its` subclass ``LCDict``. (The
:ref:`diagram of classes <prelogging-all-classes>`
shows all the classes in the `prelogging` package and their interrelations.)
``LCDictBasic`` provides the basic model of building a logging config
dict; ``LCDict`` supplies additional conveniences — for example, formatter
presets (i.e. predefined formatters), and easy access to advanced features
such as filter creation and multiprocessing-safe rotating file handlers.
The centerpiece of `prelogging` is the ``LCDict`` class.

You use the methods of these classes to add specifications of named
``Formatter``\s, ``Handler``\s, ``Logger``\s, and optional ``Filter``\s,
together with containment relations between them. Once you've done so, calling
the ``config()`` method of an ``LCDictBasic`` configures logging by passing
itself, as a ``dict``, to ``logging.config.dictConfig()``. This call creates
all the objects and linkages specified by the underlying dictionary.



`prelogging` classes and their superclasses
-------------------------------------------------------------------

.. _prelogging-all-classes:

.. figure:: ../docs/prelogging_classes-v4d.png
    :figwidth: 100%

    |br| **prelogging** classes — inheritance, and who uses whom

    +-------------------------------+-----------------------+
    | Symbol                        | Meaning               |
    +===============================+=======================+
    | .. image:: ../docs/arrsup.png | is a superclass of    |
    +-------------------------------+-----------------------+
    | .. image:: ../docs/arruse.png | uses (instantiates)   |
    +-------------------------------+-----------------------+


.. todo:: <<<<<<<<<<<<<<<< RESUME >>>>>>>>>>>>>>>>


-------------------------------------------------------------------------------

Logging configuration — with `logging`, with `prelogging`
------------------------------------------------------------------------------

.. todo:: <<<<<<<<<<<<<<<< TODO >>>>>>>>>>>>>>>>

We'll use a simple example to discuss and compare various approaches to logging
configuration — using the facilities provided by the `logging` package, and then
using `prelogging`.

Logging-configuration requirements — an example
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++


Suppose we want the following configuration:

.. _example-overview-config2:

    **Configuration requirements**

    Messages should be logged to both ``stderr`` and a file. Only messages with
    loglevel ``INFO`` or higher should appear on-screen, but all messages should
    be logged to the file. Messages to ``stderr`` should consist of just the
    message, but messages written to the file should also contain the logger
    name and the message's loglevel.

    The logfile contents should persist: the file handler should **append**
    to the logfile, rather than overwriting it each time the program using these
    loggers is run.

This suggests two handlers, each with an appropriate formatter — a ``stderr``
stream handler with level ``INFO``, and a file handler with level ``DEBUG``
or ``NOTSET``. (``NOTSET`` is the default loglevel for handlers.
Numerically less than ``DEBUG``, all loglevels are greater than or equal to it.)
Both handlers should be attached to the root logger, which should have level
``DEBUG`` to allow all messages through. The file handler should be created with
``mode='a'`` (append, not ``'w'`` for overwrite) so that the the logfile
contents can persist.

Using the example configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once this configuration is established, these logging calls:

.. code::

    import logging
    root_logger = logging.getLogger()
    # ...
    root_logger.debug("1. 0 = 0")
    root_logger.info("2. days are getting shorter")
    root_logger.debug("3. 0 != 1")
    root_logger.info("4. days are getting longer")

should produce the following ``stderr`` output:

.. code::

    2. days are getting shorter
    4. days are getting longer

and the logfile should contain (something much like) these lines:

.. code::

    root                : DEBUG   : 1. 0 = 0
    root                : INFO    : 2. days are getting shorter
    root                : DEBUG   : 3. 0 != 1
    root                : INFO    : 4. days are getting longer


Configuration with what the `logging` package provides
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The `logging` package offers two approaches to configuration:

* dynamic, using code;
* static (and then, there are two variations).

These can be thought of as *imperative* and *declarative*, respectively.
The following subsections show how each of these approaches can be used to meet
the requirements stated above.

Using dynamic configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's how to dynamically configure logging to satisfy the given requirements::

    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Create stderr handler,
    #   level = INFO, formatter = default i.e. '%(message)s';
    # attach it to root
    h_stderr = logging.StreamHandler(stream=sys.stderr)
    h_stderr.setLevel(logging.INFO)
    root.addHandler(h_stderr)

    # Create file handler, level = NOTSET (default),
    #   filename='blather_dyn_cfg.log', formatter = logger:level:msg, mode = 'a'
    # attach it to root
    logger_level_msg_fmtr = logging.Formatter('%(name)-20s: %(levelname)-8s: %(message)s')
    h_file = logging.FileHandler(filename='blather_dyn_cfg.log')
    h_file.setFormatter(logger_level_msg_fmtr)
    root.addHandler(h_file)

We've used a number of defaults. It was unnecessary to add::

    msg_fmtr = logging.Formatter('%(message)s')
    h_stderr.setFormatter(msg_fmtr)

because the same effect is achieved without them. The default ``mode`` of a
``FileHandler`` is ``'a'``, which opens the logfile for appending, as per our
requirements; thus it wasn't necessary to pass ``mode='a'`` to the
``FileHandler`` constructor. (We omitted other arguments to this constructor,
e.g. ``delay``, whose default values are suitable.) Similarly, it wasn't
necessary to set the level of the file handler, as the default level ``NOTSET``
is just what we want.

Using static configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `logging.config` submodule offers two equivalent declarative ways to specify
configuration statically:

* with a dictionary meeting various requirements (mandatory and optional keys,
  and their possible values), which is passed to ``logging.config.dictConfig()``;
* with a text file written in YAML, meeting analogous requirements,
  and passed to ``logging.config.fileConfig()``.

We'll call a dictionary that can be passed to ``dictConfig`` a *logging config
dict*. The `schema for configuration dictionaries <https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema>`_
documents the format of such dictionaries. (Amusingly, it uses YAML to do so!,
to cut down on the clutter of quotation marks. colons and curly braces.)

We'll deal only with logging config dicts, ignoring the YAML-based approach.
The Web frameworks Django and Flask configure logging with dictionaries.
(Django can accomodate YAML-based configuration, but its path of least resistance
is certainly the dict-based approach.) Dictionaries are native Python; YAML isn't.
YAML may be more readable than dictionary specifications, but `prelogging` offers
another, pure-Python solution to that problem.


Configuring our requirements statically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here's how to do so::

    import logging
    from logging import config

    config_dict = {
         'formatters': {'logger_level_msg': {'class': 'logging.Formatter',
                                             'format': '%(name)-20s: %(levelname)-8s: '
                                                       '%(message)s'}},
         'handlers': {'h_stderr': {'class': 'logging.StreamHandler',
                                   'level': 'INFO',
                                   'stream': 'ext://sys.stderr'},
                      'h_file': {'class': 'logging.FileHandler',
                                 'filename': 'blather_stat_cfg.log',
                                 'formatter': 'logger_level_msg'}},
         'root': {'handlers': ['h_stderr', 'h_file'], 'level': 'DEBUG'},
         'version': 1
    }
    logging.config.dictConfig(config_dict)

As with dynamic configuration, most keys have default values, and
in the interest of brevity we've omitted those that already suit our needs. We
didn't specify a formatter for the stream handler, nor the file
handler's mode or loglevel, and so on.


Configuration with `prelogging`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

`prelogging` provides a hybrid approach to configuration that offers the
best of both the static and dynamic worlds. The package provides a simple but
powerful API for building a logging config dict incrementally, and makes it
easy to use advanced features such as rotating log files and email handlers.
As you add and attach items, by default `prelogging` issues warnings when it
encounters possible mistakes such as referencing nonexistent entities or
redefining entities.

`prelogging` defines two classes which represent logging config dicts:
a ``dict`` subclass ``LCDictBasic``, and `its` subclass ``LCDict``. (The
:ref:`diagram of classes <prelogging-all-classes>`
shows all the classes in the `prelogging` package and their interrelations.)
``LCDictBasic`` provides the basic model of building a logging config
dict; ``LCDict`` supplies additional conveniences — for example, formatter
presets (i.e. predefined formatters), and easy access to advanced features
such as filter creation and multiprocessing-safe rotating file handlers.
The centerpiece of `prelogging` is the ``LCDict`` class.

You use the methods of these classes to add specifications of named
``Formatter``\s, ``Handler``\s, ``Logger``\s, and optional ``Filter``\s,
together with containment relations between them. Once you've done so, calling
the ``config()`` method of an ``LCDictBasic`` configures logging by passing
itself (i.e. ``self``, a ``dict``) to ``logging.config.dictConfig()``. This call
creates all the objects and linkages specified by the underlying dictionary.

Let's see this in action, applied to our example use case, and then further discuss
how the `prelogging` classes operate.

.. _config-use-case-lcdict:

Configuring our requirements using ``LCDict``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Here's how we might use ``LCDict`` to configure logging to satisfy our
:ref:`Configuration requirements _<example-overview-config>`::

    from prelogging import LCDict

    lcd = LCDict(root_level='DEBUG',
                 attach_handlers_to_root=True)
    lcd.add_stderr_handler(
                    'h_stderr',
                    formatter='msg',        # actually not needed
                    level='INFO'
    ).add_file_handler('h_file',
                       formatter='logger_level_msg',
                       filename='blather.log',
    )
    lcd.config()

First we create an ``LCDict``, which we call ``lcd`` — a logging config dict
with root loglevel ``'DEBUG'``. An ``LCDict`` has a few attributes that aren't
part of the underlying dict, including the ``attach_handlers_to_root`` flag,
which we set to ``True``. The ``add_*_handler`` methods do just what you'd
expect: each adds a subdictionary to ``lcd['handlers']`` with the respective
keys ``'h_stderr'`` and `'h_file'``, and with key/value pairs given by the
keyword parameters.

We've used a couple of the formatter presets supplied by ``LCDict`` —
``'msg'`` and ``'logger_level_msg'``. Because we pass the flag
``attach_handlers_to_root=True`` when creating ``lcd``, every
handler we add to ``lcd`` is (by default) automatically
attached to the root logger. (You can override this default by passing
``add_to_root=False`` to any ``add_*_handler`` call.)

**Notes**

* To allow chaining, as in the above example, the methods of
  ``LCDictBasic`` and ``LCDict`` generally return ``self``.

* Here's the `complete table of prelogging's formatter presets <https://pythonhosted.org/prelogging/LCDict-features-and-usage.html#index-0>`_.

-------------------------------------------------------------------------------


Structure of `prelogging`
------------------------------

.. todo?? Introductory, leading up to the diagram of all classes in package + superclasses


`prelogging` classes and their superclasses
+++++++++++++++++++++++++++++++++++++++++++++++++

.. _prelogging-all-classes2:

.. figure:: ../docs/prelogging_classes-v4d.png
    :figwidth: 100%

    |br| **prelogging** classes — inheritance, and who uses whom

    +-------------------------------+-----------------------+
    | Symbol                        | Meaning               |
    +===============================+=======================+
    | .. image:: ../docs/arrsup.png | is a superclass of    |
    +-------------------------------+-----------------------+
    | .. image:: ../docs/arruse.png | uses (instantiates)   |
    +-------------------------------+-----------------------+

-------------------------------------------------------------------------------

`LCDictBasic` Organization and Basic Usage
+++++++++++++++++++++++++++++++++++++++++++++++++++

``LCDictBasic`` provides an API for building dictionaries that specify
Python logging configurations — *logging config dicts*.
The class is fully documented in `LCDictBasic <https://pythonhosted.org/prelogging/lcdictbasic.html>`_
; this section discusses its organization and use. Everything said here about
``LCDictBasic`` will also be true of ``LCDict``; in the next section we'll
discuss unique features of the subclass.

Configuration with ``LCDictBasic``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Logging configuration involves :ref:`a small hierarchy <logging-config-classes>`
of only four kinds of entities, which can be specified in a layered way.
``LCDictBasic`` lets you build a logging config dict modularly and incrementally.
You add each logging entity and its attached entities one by one, instead of
entering a single large thicket of triply-nested dicts.

An ``LCDictBasic`` instance *is* a logging config dict. It inherits from
``dict``, and its methods —``add_formatter``, ``add_handler``, ``add_logger``,
``attach_logger_handlers`` and so on — operate on the underlying dictionary,
breaking down the process of creating a logging config dict into basic steps.

While configuring logging, you give a name to each of the entities that you add.
(Strictly speaking, you're adding *specifications* entities)
When adding a higher-level entity, you
identify its constituent lower-level entities by name.

Once you’ve built an ``LCDictBasic`` meeting your requirements, you configure
logging by calling the object’s ``config`` method, which passes itself (as
a dict) to `logging.config.dictConfig() <https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig>`_.

Specification order
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``Formatter``\s and ``Filter``\s (if any) don't depend on any other
  logging entities, so they should be specified first.
* Next, specify ``Handler``\s (and any ``Filter``\s they use).
* Finally, specify ``Logger``\s, indicating their use of already-defined
  ``Handler``\s (and ``Filter``\s, if any).

**Note**:
``LCDictBasic`` has dedicated methods for configuring the root logger (setting
its level, attaching handlers and filters to it), but you can also use the
class's general-purpose handler methods for this, identifying the root logger by
its name, ``''``.

Typically, ``Filter``\s aren't required, and then, setting up logging
involves just these steps:

1. specify ``Formatter``\s
2. specify ``Handler``\s that use the ``Formatter``\s
3. specify ``Logger``\s that use the ``Handler``\s.

**Note**: In common cases, such as the :ref:`configuration requirements <example-overview-config>`
example in the previous chapter and :ref:`its solution <config-use-case-lcdict>`,
``LCDict`` eliminates the first step, and makes the last step trivial when only
the root logger will have handlers.

Methods and properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``add_*`` methods of ``LCDictBasic`` let you specify new, named logging
entities. Each call to one of the ``add_*`` methods adds an item
to one of the subdictionaries ``'formatters'``, ``'filters'``, ``'handlers'``
or ``'loggers'``. In each such call, you can specify all of the data for
the entity that the item describes — its loglevel, the other entities it will
use, and any type-specific information, such as the stream that a ``StreamHandler``
will write to.

You can specify all of an item's dependencies in an ``add_*`` call,
using names of previously added items, or you can add dependencies
subsequently with the ``attach_*`` methods. In either case, you assign a list
of values to a key of the item: for example, the value of the ``handlers`` key
for a logger is a list of zero or more names of handler items.

The ``set_*`` methods let you set single-valued fields (loglevels; the
formatter, if any, of a handler).

In addition to the ``config`` method, which we've already seen, ``LCDictBasic``
has methods ``check`` and ``dump``. The properties of ``LCDictBasic`` correspond
to the top-level subdictionaries of the underlying dict. See
`LCDictBasic <https://pythonhosted.org/prelogging/lcdictbasic.html>`_
for details.

Keyword parameters
^^^^^^^^^^^^^^^^^^^^^

Keyword parameters of the ``add_*`` methods are consistently snake_case versions
of the corresponding keys that occur in statically declared logging config
dicts; their default values are the same as those of `logging`.
(There are just a few — rare, documented — exceptions to these sweeping
statements. One noteworthy exception: ``class_`` is used instead of ``class``,
as the latter is a Python reserved word and can't be a parameter.)

For example, the keyword parameters of ``add_file_handler`` are keys that can
appear in a (sub-sub-)dictionary of configuration settings for a file handler;
the keyword parameters of ``add_logger`` are keys that can appear in the
(sub-sub-)dicts that configures loggers. In any case, all receive sensible
default values consistent with `logging`.

Items of a logging config dict
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here's what a minimal, "blank" logging config dict looks like::

    >>> from prelogging import LCDictBasic
    >>> d = LCDictBasic()
    >>> d.dump()        # prettyprint the underlying dict
    {'filters': {},
     'formatters': {},
     'handlers': {},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': [], 'level': 'WARNING'},
     'version': 1}

Every logging config dict built by `prelogging` has the five subdictionaries
and two non-dict items shown; no `prelogging` methods remove any of these items
or add further items. The ``LCDictBasic`` class exposes the subdictionaries
as properties:
``formatters``, ``filters``, ``handlers``, ``loggers``, ``root``.
``root`` is a dict containing settings for that special logger. Every other
subdict contains keys that are names of entities of the appropriate kind;
the value of each such key is a dict containing configuration settings for
the entity. In an alternate universe, ``'root'`` and its value (the ``root``
subdict) could be just a special item in the ``loggers`` subdict; but
logging config dicts aren't defined that way.

Properties
__________________

An ``LCDictBasic`` makes its top-level subdictionaries available as properties
with the same names as the keys: ``d.formatters is d['formatters']`` is true,
so is ``d.handlers is d['handlers']``, and likewise for ``d.filters``,
``d.loggers``, ``d.root``. For example, adding a formatter ``'simple'``
to ``d``::

    >>> d.add_formatter('simple')

changes the ``formatters`` collection to::

    >>> d.formatters                # ignoring whitespace
    {'simple': {'class': 'logging.Formatter',
                'format': None}
    }

Methods, terminology
^^^^^^^^^^^^^^^^^^^^^^^^^


The ``add_*`` methods
__________________________

The basic ``add_*`` methods are these four::

    add_formatter(self, name, format='', ... )
    add_filter(self, name, ... )
    add_handler(self, name, level='NOTSET', formatter=None, filters=None, ... )
    add_logger(self, name, level='NOTSET', handlers=None, filters=None, ...  )

``LCDictBasic`` also defines three special cases of ``add_handler``::

    add_stream_handler
    add_file_handler
    add_null_handler

which correspond to all the handler classes defined in the ``logging`` module.
(Similarly, ``LCDict`` defines ``add_*_handler`` methods for many of the handler
classes defined in ``logging.handlers`` — details below in :ref:`supported-handlers`.)

Each ``add_*`` method adds an item to (or replaces an item in) the corresponding
subdictionary. For example, when you add a formatter::

    >>> _ = d.add_formatter('fmtr', format="%(name)s %(message)s")

you add an item to ``d.formatters`` whose key is ``'fmtr'`` and whose value is
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
                         'mode': 'a'}},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': [], 'level': 'WARNING'},
     'version': 1}

Similarly, ``add_filter`` and ``add_logger`` add items to the ``filters`` and
``loggers`` dictionaries respectively.

The ``attach_*_*`` methods
____________________________

The configuring dict of a handler has an optional ``'filters'`` list;
the configuring dict of a logger can have a ``'filters'`` list and/or
a ``'handlers'`` list. The ``attach_``\ *entity*\ ``_``\ *entities* methods
extend these lists of filters and handlers::

    attach_handler_filters(self, handler_name, * filter_names)

    attach_logger_handlers(self, logger_name, * handler_names)
    attach_logger_filters(self, logger_name, * filter_names)

    attach_root_handlers(self, * handler_names)
    attach_root_filters(self, * filter_names)

All these methods attach *entities* to an *entity*. Each takes a variable number
of *entities* as their final parameters, and attach them to *entity*, which
precedes them in the parameter list. The method names reflect the parameter order.

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
                         'mode': 'a'}},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': ['fh', 'console'], 'level': 'WARNING'},
     'version': 1}

The ``set_*_*`` methods
__________________________

These methods modify a single value — a loglevel, or a formatter::

    set_handler_level(self, handler_name, level)
    set_root_level(self, root_level)
    set_logger_level(self, logger_name, level)
    set_handler_formatter(self, handler_name, formatter_name)

-------------------------------------------------------------------------------

.. _lcdict-features:

`LCDict` Features and Usage
+++++++++++++++++++++++++++++++++

``LCDict`` subclasses ``LCDictBasic`` to contribute additional
conveniences. The class is fully documented in `LCDict <https://pythonhosted.org/prelogging/lcdict.html>`_.
In this chapter we describe the features it adds:

* :ref:`formatter presets <formatter_presets>`
* :ref:`add_*_handler methods for several classes in logging.handlers <supported-handlers>`
* :ref:`optional automatic attaching of handlers to the root logger as they're added <auto-attach-handlers-to-root>`
* :ref:`easy multiprocessing-safe logging <easy-mp-safe-logging>`
* :ref:`simplified creation and use of filters <filters>`.

.. _formatter_presets:

Formatter presets
~~~~~~~~~~~~~~~~~~~~~

We've already seen simple examples of adding new formatters using
``add_formatter``. See the documentation of that method in
`LCDictBasic <https://pythonhosted.org/prelogging/lcdictbasic.html>`_
for details of its parameters and their possible values.

As our :ref:`first example <config-use-case-lcdict>` indicated,
often it's not necessary to specify formatters from scratch,
because ``LCDict`` provides about a dozen formatter *presets* —
predefined formatter specifications which cover many needs.
You can use the name of any of these presets as the ``formatter`` argument
to any ``LCDict`` method that can take a *formatter* argument
(thus, the ``add_*_handler`` methods and ``set_handler_formatter``).

Here are all the formatter presets:

.. _LCDict-using-formatter-presets:
.. _preset-formatters:

.. index:: preset formatters (LCDict), formatter presets (LCDict)

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

Formatter presets are added to an ``LCDict`` "just in time", when they're used::

    >>> lcd = LCDict()
    >>> # The underlying dict of a "blank" LCDict
    >>> #   is the same as that of a blank LCDictBasic --
    >>> #   lcd.formatters is empty:
    >>> lcd.dump()
    {'disable_existing_loggers': False,
     'filters': {},
     'formatters': {},
     'handlers': {},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': [], 'level': 'WARNING'},
     'version': 1}

    >>> # Using the 'level_msg' preset adds it to lcd.formatters:
    >>> _ = lcd.add_stderr_handler('console', 'level_msg')
    >>> lcd.dump()
    {'disable_existing_loggers': False,
     'filters': {},
     'formatters': {'level_msg': {'class': 'logging.Formatter',
                                  'format': '%(levelname)-8s: %(message)s'}},
     'handlers': {'console': {'class': 'logging.StreamHandler',
                              'formatter': 'level_msg',
                              'level': 'WARNING',
                              'stream': 'ext://sys.stderr'}},
     'incremental': False,
     'loggers': {},
     'root': {'handlers': [], 'level': 'WARNING'},
     'version': 1}

Only ``'level_msg'`` has been added to ``lcd.formatters``.


.. ------------------------------------------------------

.. _supported-handlers:

Handler classes encapsulated by ``LCDict``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
optional "locking" support in most cases:

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

Automatically attaching handlers to the root logger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because handlers are so commonly attached to the root logger,
``LCDict`` makes it easy to do that. Two parameters and their defaults
govern this:

* The initializer method ``LCDict.__init__`` has a boolean parameter
  ``attach_handlers_to_root`` [default: ``False``].

  Each instance saves the value passed to its constructor, and exposes it as the
  read-only property ``attach_handlers_to_root``.
  When ``attach_handlers_to_root`` is true, by default the
  handler-adding methods of this class automatically attach handlers to
  the root logger after adding them to the ``handlers`` subdictionary.
  |br10th|
  |br10th|
* All ``add_*_handler`` methods **called on an** ``LCDict``, as well as
  the ``clone_handler`` method, have an ``attach_to_root`` parameter
  [type: ``bool`` or ``None``; default: ``None``].
  The ``attach_to_root`` parameter
  allows overriding of the value ``attach_handlers_to_root`` passed to
  the constructor.

  The default value of ``attach_to_root``
  is ``None``, which is interpreted to mean: use the value of
  ``attach_handlers_to_root`` passed to the constructor. If ``attach_to_root``
  has any value other than ``None``,
  the handler will be attached *iff* ``attach_to_root`` is true/truthy.

Thus, if ``lcd`` is an ``LCDict`` created with ``attach_handlers_to_root=True``,

    ``lcd = LCDict(attach_handlers_to_root=True, ...)``

you can still add a handler to ``lcd`` without attaching it to the root::

    lcd.add_stdout_handler('stdout', attach_to_root=False, ...)

Similarly, if lcd`` is created with ``attach_handlers_to_root=False`` (the default)::

    ``lcd = LCDict(...)``

you can attach a handler to the root as soon as you add it to ``lcd``::

    lcd.add_file_handler('fh', filename='myfile.log', attach_to_root=True, ...)

without having to subsequently call ``lcd.attach_root_handlers('fh', ...)``.


.. _easy-mp-safe-logging:

Easy multiprocessing-safe logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As we've mentioned, most recently in the this chapter's earlier section
:ref:`LCDict-handler-classes-encapsulated`,
`prelogging` provides multiprocessing-safe ("locking") versions of the essential
handler classes that write to the console, streams, files, rotating files, and
syslog. These subclasses of handler classes defined by `logging` are documented in
`locking handlers <https://pythonhosted.org/prelogging/locking_handlers.html>`_.
The following ``LCDict`` methods:

  | ``add_stream_handler``
  | ``add_stderr_handler``
  | ``add_stdout_handler``
  | ``add_file_handler``
  | ``add_rotating_file_handler``
  | ``add_syslog_handler``

can create either a standard, `logging` handler or a locking version thereof.
Two keyword parameters (with the same name: ``locking``) and their defaults
govern which type of handler will be created:

* The initializer method ``LCDict.__init__`` has a Boolean parameter
  ``locking`` [default: ``False``].

  Each ``LCDict`` instance saves the value passed to its constructor,
  and exposes it as the read-only property ``locking``.
  When ``locking`` is true, by default the ``add_*_handler`` methods listed above
  will create locking handlers.
  |br10th|
  |br10th|
* The ``add_*_handler`` methods listed above have a ``locking`` parameter
  [type: ``bool`` or ``None``; default: ``None``], which
  allows overriding of the value ``locking`` passed to the constructor.

  The default value of the ``add_*_handler`` parameter ``locking``
  is ``None``, which is interpreted to mean: use the value of
  ``locking`` passed to the constructor. If the ``add_*_handler`` parameter
  ``locking`` has any value other than ``None``,
  a locking handler will be created *iff* the parameter's value is true/truthy.


.. _easy-filter-creation:
.. _filters:

Simplified creation and use of filters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Filter allow finer control than mere loglevel comparison over which messages
actually get logged.

There are two kinds of filters: class filters and callable filters.
``LCDict`` provides a pair of convenience methods, ``add_class_filter`` and
``add_callable_filter``, which are much easier to use than the lower-level
``LCDictBasic`` method ``add_filter``.

In Python 2, the `logging` module imposes a fussy requirement on callables
that can be used as filters, which the Python 3 implementation of `logging`
removes. The ``add_callable_filter`` method provides a single, sane interface
for adding callable filters that works in both Python versions.

The use of filters, and of these methods, is described and illustrated in the section
`Simplified creation and use of filters <https://pythonhosted.org/prelogging/LCDict-features-and-usage.html#simplified-creation-and-use-of-filters>`_.
of the full documentation.

-------------------------------------------------------------------------------

.. _config-abc:

Using ``LCDictBuilderABC``
-------------------------------

One way for a larger program to configure logging is to pass around an
``LCDict`` to the different "areas" of the program, each area contributing
specifications of its desired formatters, filters, handlers and loggers.
The ``LCDictBuilderABC`` class provides a mini-microframework that automates
this approach: each area of a program need only define an ``LCDictBuilderABC``
subclass and override its method ``add_to_lcdict(lcd)``, where it contributes
its specifications by calling methods on ``lcd``.

The `LCDictBuilderABC <https://pythonhosted.org/prelogging/LCDictBuilderABC.html>`_
documentation describes how that class and its two methods operate. The test
``tests/test_lcdict_builder.py`` illustrates using the class to configure logging
across multiple modules.

.. _migration-dynamic:

Migrating a project that uses dynamic configuration to `prelogging`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

First a caveat: If your program uses the `logging` API throughout the course of
its execution to create or (re)configure logging entities, then
migration to `prelogging` may offer little gain: many of the runtime calls to
`logging` methods probably can't be replaced. In particular, obviously `prelogging`
provides no means to delete or detach logging entities.

However, if your program uses the `logging` API to configure logging
only at startup, in a "set it and forget it" way, then it's probably easy
to migrate it to `prelogging`. Benefits of doing so include clearer, more
concise code, and access to the various amenities of `prelogging`.

.. _migration-static:

Migrating a project that uses static dict-based configuration to `prelogging`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A common pattern for a large program that uses static dict-based configuration
is to pass around a single (logging config) dict to each "area" of the program;
each "area" adds its own required entities and possibly modifies those already
added; finally a top-level routine passes the dict to ``logging.config.dictConfig``.

Let's suppose that each program "area" modifies the logging config dict in
a function called ``add_to_config_dict(d: dict)``. These ``add_to_config_dict``
functions performs dict operations on the parameter ``d`` such as

    ``d['handlers']['another_formatter'] = { ... }``

and

    ``d.update( ... )``.

*Assuming your* ``add_to_config_dict`` *functions use "duck typing" and work
on any parameter* ``d`` *such that* ``isinstance(d, dict)`` *is true, they
should continue to work properly if you pass them an* LCDict.

Thus, the ``add_to_config_dict`` function specific to each
program area can easily be converted to an ``add_to_lcdict(cls, lcd: LCDict)``
classmethod of an `LCDictBuilderABC <https://pythonhosted.org/prelogging/LCDictBuilderABC.html>`_
subclass specific to that program area.

---------------------------------------------------------------------------

.. todo::
    (watch this space)
