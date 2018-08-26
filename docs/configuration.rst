.. include:: _global.rst

Configuration — with `logging`, and with `prelogging`
=======================================================

We'll use a simple example to discuss and compare various approaches to logging
configuration — using the facilities provided by the `logging` package, and then
using `prelogging`.

Logging configuration requirements — example
------------------------------------------------------------


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
stream handler with level ``INFO``, and a file handler with level ``DEBUG``
or ``NOTSET``. (``NOTSET`` is the default loglevel for handlers.
Numerically less than ``DEBUG``, all loglevels are greater than or equal to it.)
Both handlers should be attached to the root logger, which should have level
``DEBUG`` to allow all messages through. The file handler should be created with
``mode='a'`` (for append, not ``'w'`` for overwrite) so that existing logfile
contents persist.

Using the example configuration
+++++++++++++++++++++++++++++++++++

Once this configuration is established, these logging calls:

.. code::

    import logging
    root_logger = logging.getLogger()
    # ...
    root_logger.debug("1. 0 = 0")
    root_logger.info("2. Couldn't create new Foo object")
    root_logger.debug("3. 0 != 1")
    root_logger.warning("4. Foo factory raised IndexError")

should produce the following ``stderr`` output:

.. code::

    2. Couldn't create new Foo object
    4. Foo factory raised IndexError

and the logfile should contain (something much like) these lines:

.. code::

    root                : DEBUG   : 1. 0 = 0
    root                : INFO    : 2. Couldn't create new Foo object
    root                : DEBUG   : 3. 0 != 1
    root                : WARNING : 4. Foo factory raised IndexError


Meeting the configuration requirements with `logging`
---------------------------------------------------------------

The `logging` package offers two approaches to configuration:

* dynamic, using code;
* static (and then, there are two variations).

These can be thought of as *imperative* and *declarative*, respectively.
The following subsections show how each of these approaches can be used to meet
the requirements stated above.

Using dynamic configuration
+++++++++++++++++++++++++++++++++++++++++++++

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
``FileHandler`` is ``a``, which opens the logfile for appending, as per our
requirements; thus it wasn't necessary to pass ``mode='a'`` to the
``FileHandler`` constructor. (We omitted other arguments to this constructor,
e.g. ``delay``, whose default values are suitable.) Similarly, it wasn't
necessary to set the level of the file handler, as the default level ``NOTSET``
is just what we want.

Advantages of dynamic configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* *Hierarchy of logging entities respected*

  Formatters must be created before the handlers that use them;
  handlers must be created before the loggers to which they're attached.

  You can configure the entities of logging (formatters, optional filters,
  handlers, loggers) one by one, in order, starting with those that don't
  depend on other entities, and proceeding to those that use entities
  already defined.
  |br10th|
  |br10th|
* *Methods of the `logging` API provide reasonable defaults*

  With static configuration, certain fussy defaults must be specified explicitly.
  |br10th|
  |br10th|
* *Error prevention*

  For instance, there's no way to attach things that simply don't exist.
  |br10th|
  |br10th|
* *Fine-grained error detection*

  If you use a nonexistent keyword argument, for example, the line in which it
  occurs gives an error; you don't have to wait until issuing a final
  ``dictConfig`` call to learn that something was amiss.

  Thus it's easier to debug: each step taken is rather small, and you can fail
  faster than when configuring from an entire dictionary.


Disadvantages of dynamic configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    * *Low-level methods, inconsistent API*

      The ``Handler`` base class takes a keyword argument ``level``; however,
      its subclass ``StreamHandler`` takes a keyword argument ``stream``,
      but doesn't recognize ``level``. Thus we couldn't concisely say::

          h_stderr = logging.StreamHandler(level=logging.INFO, stream=sys.stderr)

      but had to call ``h_stderr.setLevel`` after constructing the handler.
      |br10th|
      |br10th|
    * *In `logging`, only loggers have names; formatters, handlers and filters
      don't*

      Thus we have to use Python variables to reference the various
      logging entities which we create and connect. If another part of the
      program later wanted to access, say, the file handler attached to the
      root logger, the only way it could do so would be by iterating through
      the ``handlers`` collection of the root and examining the type of each::

          root = logging.getLogger()
          fh = next(h for h in root.handlers if isinstance(h, logging.FileHandler))

    * *Somehow it winds up more even verbose than static dictionaries*

      The methods are low-level, and many boilerplate passages recur
      in dynamic configuration code.


Using static configuration
++++++++++++++++++++++++++++++++++++++++++

The `logging.config` submodule offers two equivalent ways to specify
configuration statically:

* with a dictionary meeting various requirements (mandatory and optional keys,
  and their values), which is passed to ``logging.config.dictConfig()``;
  |br10th|
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Advantages of static configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* *Logging entities are referenced by name*

  You give a name to every logging entity you specify, and then refer
  to it by that name when attaching it to higher-level entities.
  (It's true that after the call to ``dictConfig``, only the names of loggers
  endure [*as per the documentation! but see :ref:`Note <HANDLER_NAMES_TOO>` below*];
  however, that's a separate issue — a deficiency of `logging`, not of static
  configuration.)
  |br10th|
  |br10th|
* *It's arguably more natural to specify configuration in a declarative way*,
  especially for the typical application which will "set it and forget it".

.. _HANDLER_NAMES_TOO:
    .. note::
        Although it's not documented (as of Python 3.7), every ``Handler``
        has a read-write property ``name``; moreover, the name used in a logging
        config dict to identify a handler becomes the ``Handler`` object's ``.name``.
        It seems that `logging` only uses the ``name`` property during configuration.

Disadvantages of static configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* *Not very good error detection* (none until the ``dictConfig`` call)
  |br10th|
  |br10th|
* *Some boilerplate key/value pairs*
  |br10th|
  |br10th|
* *Lots of noise* — a thicket of nested curly braces, quotes, colons, etc.

  Triply-nested dicts are hard to read.
  |br10th|
  |br10th|
* *Logging config dicts seem complex*

  At least on first exposure to static configuration, it's not easy to
  comprehend a medium- to large-sized dict of dicts of dicts, in which many
  values are lists of keys occurring elsewhere in the structure.

Assessment
+++++++++++++++++++++++++++++++++++++++++++++++++++

As we've seen, both approaches to configuration offered by the `logging`
package have virtues, but both have shortcomings:

* Its API, mostly dedicated to dynamic configuration, is at once complex and
  limited.
* With static configuration, no warnings are issued and no error checking occurs
  until ``dictConfig`` (or ``fileConfig``) is called.
* Of the various kinds of entities that `logging` constructs, only loggers have
  (documented) names, which, as seen above, can lead to various conundrums and
  contortions.

  Said another way, once logging is configured, only the names of ``Logger``\s
  endure. `logging` retains *no associations* between the names you used to
  specify ``Formatter``\s, ``Handler``\s and ``Filter``\s, and the objects
  constructed to your specifications; you can't access those objects by any
  name.

To this list, we might add the general observation that the entire library is
written in thoroughgoing camelCase (except for inconsistencies, such as
``levelname`` in format strings).

----------------------------------

Configuration with `prelogging`
--------------------------------------

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
presets (predefined formatters), and easy access to advanced features
such as filter creation and multiprocessing-safe rotating file handlers.
The centerpiece of `prelogging` is the ``LCDict`` class.

You use the methods of these classes to add specifications of named
``Formatter``\s, ``Handler``\s, ``Logger``\s, and optional ``Filter``\s,
together with containment relations between them. Once you've done so, calling
the ``config()`` method of an ``LCDictBasic`` configures logging by passing
itself, as a ``dict``, to ``logging.config.dictConfig()``. This call creates
all the objects and linkages specified by the underlying dictionary.

Let's see this in action, applied to our use case, and then further discuss
how the `prelogging` classes operate.

.. _config-use-case-lcdict:

Configuring our requirements using ``LCDict``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Here's how we might use ``LCDict`` to configure logging to satisfy our
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
keyword parameters.

We've used a couple of `prelogging`'s formatter presets —
``'msg'`` and ``'logger_level_msg'``. Because we pass the flag
``attach_handlers_to_root=True`` when creating ``lcd``, every
handler we add to ``lcd`` is (by default) automatically
attached to the root logger. (You can override this default by passing
``add_to_root=False`` to any ``add_*_handler`` call.)

**Notes**

* To allow chaining, as in the above example, the methods of
  ``LCDictBasic`` and ``LCDict`` generally return ``self``.

* Here's the :ref:`complete table of prelogging's formatter presets <preset-formatters-table>`.

Configuring our requirements using ``LCDictBasic``
++++++++++++++++++++++++++++++++++++++++++++++++++++

It's instructive to see how to achieve :ref:`the example configuration <example-overview-config>`
using only ``LCDictBasic``, foregoing the conveniences of ``LCDict``. The code
becomes just a little less terse. Now we have to add two formatters,
and we must explicitly attach the two handlers to the root logger. We've
commented those passages with ``# NEW``::

    from prelogging import LCDictBasic

    lcd = LCDictBasic(root_level='DEBUG')

    # NEW
    lcd.add_formatter('msg',
                      format='%(message)s'
    ).add_formatter('logger_level_msg',
                    format='%(name)-20s: %(levelname)-8s: %(message)s'
    )

    lcd.add_handler('h_stderr',
                    formatter='msg',
                    level='INFO',
                    class_='logging.StreamHandler',
    ).add_file_handler('h_file',
                       formatter='logger_level_msg',
                       level='DEBUG',
                       filename='blather.log',
    )

    # NEW
    lcd.attach_root_handlers('h_stderr', 'h_file')

    lcd.config()


Summary
+++++++++++++++++
As the preceding example hopefully shows, `prelogging` offers an attractive
way to configure logging, one that's more straightforward, concise and easier
on the eyes than the facilities provided by the `logging` package itself.
The following chapters discuss basic organization and usage of ``LCDictBasic``
and ``LCDict``. Later chapters present techniques and recipes showing how to
use these classes to get more out of logging.
