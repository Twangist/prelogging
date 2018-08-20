`LCDictBasic` Organization and Basic Usage
===============================================

``LCDictBasic`` provides an API for building dictionaries that specify
Python logging configurations — *logging config dicts*.
The class is fully documented in :ref:`LCDictBasic`; this chapter discusses its
organization and use. Everything said here about ``LCDictBasic`` will also be
true of its subclass ``LCDict``, whose unique features we'll discuss in the next
chapter.

Configuration with ``LCDictBasic``
----------------------------------

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
(Strictly speaking, you're adding *specifications* of logging objects.)
When adding a higher-level entity, you identify its constituent lower-level
entities by name.

Once you’ve built an ``LCDictBasic`` meeting your requirements, you configure
logging by calling that object’s ``config`` method, which passes it (``self``,
a dict) to `logging.config.dictConfig() <https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig>`_.

Specification order
++++++++++++++++++++

* ``Formatter``\s and ``Filter``\s (if any) don't depend on any other
  logging entities, so they should be specified first.
* Next, specify ``Handler``\s, referencing any ``Formatter``\s and ``Filter``\s that the handlers use.
* Finally, specify ``Logger``\s, referencing any ``Handler``\s (and possibly ``Filter``\s) that they use.

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
--------------------------------

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
to the top-level subdictionaries of the underlying dict. See :ref:`LCDictBasic`
for details.

Keyword parameters
+++++++++++++++++++++++

Keyword parameters of the ``add_*`` methods are consistently snake_case versions
of the corresponding keys that occur in statically declared logging config
dicts; their default values are the same as those of `logging`.
(There are just a few — rare, documented — exceptions to these sweeping
statements. One noteworthy exception: ``class_`` is used instead of ``class``,
as the latter is a Python reserved word and can't be a parameter.)

For example, the keyword parameters of ``add_file_handler`` are keys that can
appear in a (sub-sub-)dictionary of configuration settings for a file handler;
the keyword parameters of ``add_logger`` are keys that can appear in the
(sub-sub-)dicts that configure loggers. In any case, all receive sensible
default values consistent with `logging`.

Items of a logging config dict
++++++++++++++++++++++++++++++++

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
The last, ``root``, is a dict containing settings for that special logger.
Every other subdict contains keys that are names of entities of the appropriate
kind; the value of each such key is a dict containing configuration settings for
the entity. In an alternate universe, ``'root'`` and its value (the ``root``
subdict) could be just a special item in the ``loggers`` subdict; but
logging config dicts aren't defined that way.

Properties
~~~~~~~~~~~~
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
+++++++++++++++++++++


The ``add_*`` methods
~~~~~~~~~~~~~~~~~~~~~~~

The basic ``add_*`` methods are these four::

    add_formatter(self, name, format='', ... )
    add_filter(self, name, ... )
    add_handler(self, name, level='NOTSET', formatter=None, filters=None, ... )
    add_logger(self, name, level='NOTSET', handlers=None, filters=None, ...  )

``LCDictBasic`` also defines three special cases of ``add_handler``::

    add_stream_handler
    add_file_handler
    add_null_handler

which correspond to all the handler classes defined in the core module of ``logging``.
(:ref:`LCDict <LCDict>` defines methods for many of the handler classes defined in
``logging.handlers`` -- see the later section, :ref:`supported-handlers`.)

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The configuring dict of a handler has an optional ``'filters'`` list;
the configuring dict of a logger can have a ``'filters'`` list and/or
a ``'handlers'`` list. The ``attach_``\ *entity*\ ``_``\ *entities* methods
extend these lists of filters and handlers::

    attach_handler_filters(self, handler_name, * filter_names)

    attach_logger_handlers(self, logger_name, * handler_names)
    attach_logger_filters(self, logger_name, * filter_names)

    attach_root_handlers(self, * handler_names)
    attach_root_filters(self, * filter_names)

**Note**:
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~

These methods modify a single value — a loglevel, or a formatter::

    set_handler_level(self, handler_name, level)
    set_root_level(self, root_level)
    set_logger_level(self, logger_name, level)
    set_handler_formatter(self, handler_name, formatter_name)

**Note**: We might have named the last method "attach_handler_formatter", as the
handler-uses-formatter relation is another example of an association between two
different kinds of logging entities. However, further reflection reveals that
a formatter is not "attached" in the sense of all the other ``attach_*_*``
methods. A handler has at most one formatter, and "setting" a handler's
formatter replaces any formatter previously set; in contrast, the ``attach_*_*``
methods only append to and extend collections of filters and handlers, and never
delete or replace items. Hence "set_handler_formatter".


--------------------------------------------------

.. _warnings-consistency-checking:

`prelogging` warnings and consistency checking
-----------------------------------------------------------

Here's another benefit provided by `prelogging` that you don't enjoy by handing
a (possibly large) dict to `logging.config.dictConfig()``:
`prelogging` detects certain dubious practices and probable mistakes,
and optionally prints warnings about them. In any case it automatically
prevents some of those detected problems, such as attempting to attach
a handler to a logger multiple times, or referencing an entity that doesn't exist
(because you haven't added it yet, or mistyped its name).


The inner class ``LCDictBasic.Warnings``
++++++++++++++++++++++++++++++++++++++++++++++++++++

``LCDictBasic`` has an inner class ``Warnings`` that defines bit-field "constants",
or flags, which indicate the different kinds of anomalies that `prelogging` checks for, corrects
when that's sensible, and optionally reports on with warning messages.

+--------------------------+-------------------------------------------------------------+
|| ``Warnings`` "constant" || Issue a warning when...                                    |
||                         ||                                                            |
+==========================+=============================================================+
|| ``REATTACH``            || attaching an entity {formatter/filter/handler}             |
||                         || to another entity that it's already attached to            |
|| ``REDEFINE``            || overwriting an existing definition of an entity            |
|| ``ATTACH_UNDEFINED``    || attaching an entity that hasn't yet been added ("defined") |
|| ``REPLACE_FORMATTER``   || changing a handler's formatter                             |
+--------------------------+-------------------------------------------------------------+

The class also defines a couple of shorthand "constants"::

    DEFAULT = REATTACH + REDEFINE + ATTACH_UNDEFINED
    ALL     = REATTACH + REDEFINE + ATTACH_UNDEFINED + REPLACE_FORMATTER


.. _init-warnings:

``warnings`` — property, parameter of ``__init__``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The value of the ``warnings`` parameter of the ``LCDictBasic`` constructor can
be any combination of the "constants" in the above table. Its default value is,
naturally, ``Warnings.DEFAULT``. The value of this parameter is saved
as an ``LCDictBasic`` instance attribute, which is exposed by the read-write
``warnings`` property.

When one of these flags is "on" in the ``warnings`` property and the corresponding
kind of offense occurs, `prelogging` prints a warning message
to stderr, indicating the source file and line number of the offending method
call.

REATTACH (default: reported)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`prelogging` detects and eliminates duplicates in lists of handlers or filters
that are to be attached to higher-level entities. If ``REATTACH`` is "on"
in ``warnings``, `prelogging` will report duplicates.


REDEFINE (default: reported)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If this flag is "on" in ``warnings``, `prelogging` warns when
an existing definition of an entity is replaced, for example by calling
``add_handler('h', ...)`` twice.

.. _ATTACH_UNDEFINED:

``ATTACH_UNDEFINED`` (default: reported)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If this flag is "on" in ``warnings``, `prelogging` detects when an as-yet
undefined entity is associated with another entity that uses it:

* undefined formatter assigned to a handler
* undefined filter attached to a handler
* undefined filter attached to a logger
* undefined handler attached to a logger


``REPLACE_FORMATTER`` (default: not reported)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If this flag is "on" in ``warnings``, `prelogging` warns when
a handler that already has a formatter is given a new formatter.


.. _check:

Consistency checking — the ``check`` method
+++++++++++++++++++++++++++++++++++++++++++++++++

This method checks for references to "undefined" entities, as described above
for :ref:`ATTACH_UNDEFINED <ATTACH_UNDEFINED>`. If any exist, ``check`` reports
that, and raises ``KeyError``; otherwise, it returns ``self``.

If the ``Warnings.REATTACH`` flag of the ``warnings`` property is "off",
``config()`` calls ``check()`` automatically before calling ``logging.config.config()``.
