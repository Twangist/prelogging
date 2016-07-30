# coding=utf-8

from __future__ import print_function
from .six import PY2
import logging
import logging.config

__author__ = "Brian O'Neill"

__doc__ = """ \
``LoggingConfigDict`` provides an API for building dictionaries that specify
Python logging configuration -- *logging config dicts*.

Entering a logging config dict as static data requires many nested curly
braces, colons, single-quoted keywords, and boilerplate default key/value pairs.
Such dicts are significantly nested, and keys often appear among
the data, as back-references to things "already defined".

But logging configuration involves a small hierarchy of only four kinds of
entities — formatters, handlers, loggers and, optionally, filters —
which can be specified in a layered way.

``LoggingConfigDict`` lets you build a logging config dict modularly and
incrementally. It flattens the process of specifying the dict, letting you
define each entity one by one, instead of entering a thicket of nested dicts.

A ``LoggingConfigDict`` instance *is* a logging config dict. It inherits from
``dict``, and its methods —``add_formatter``, ``add_handler``, ``add_logger``,
and so on — operate on the underlying dictionary, breaking down the process
of creating a logging config dict into basic steps:

    1. Create a ``LoggingConfigDict``, optionally specifying the level of
       the root handler.

    2. Add formatter specifications with ``add_formatter()``.

    3. Add any filter specifications with ``add_filter()``.

    4. Add handler specifications with ``add_handler()`` and/or
       ``add_file_handler()``, specifying its loglevel, and referring by name to
       a formatter (and possibly filters) already specified in previous steps.
       Other methods let you attach filters to a previously added handler
       and set its loglevel.

    *In steps 2. – 4. you give each thing specified a name, by which you refer
    to it in subsequent steps when attaching the thing to other, higher-level
    things.*

    5. If desired, configure the root logger using ``attach_root_handlers()``,
       ``attach_root_filters()`` and/or ``set_root_level()``, referring by name
       to handlers and filters already specified in previous steps.

    6. Add specifications for any non-root loggers with ``add_logger()``.
       Specify the handlers and filters of a logger by name, using the
       ``handlers`` and ``filters`` keyword parameters. You can also attach
       handlers and filters to an already-added logger, and set its loglevel.

    *Steps 2. and 3. can be interchanged, likewise 5. and 6.*

Keyword parameters of the ``add_*`` methods are the very same keys that occur in
the sub-subdictionaries of the corresponding kind of logging entities (with just
one exception: ``class_`` instead of ``class``). All receive correct and/or
sensible default values.

Once you've built a ``LoggingConfigDict`` meeting your requirements, you
configure logging by calling the object's ``config`` method, which simply
passes itself (a dict) to
`logging.config.dictConfig() <https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig>`_.

**Note**: The `lcd` class :ref:`ConfiguratorABC` defines an alternate,
higher-level mini-framework for configuring logging, which calls ``config``
for you.
"""


class LoggingConfigDict(dict):
    """
    .. include:: _global.rst

    *   In this class as well as in :ref:`LoggingConfigDictEx`, "level" always
        means the ``str`` name of the level, e.g. ``'DEBUG'``, not the numeric
        value ``logging.DEBUG``. A level name, in short — one of ``'DEBUG'``,
        ``'INFO'``, ``'WARNING'``, ``'ERROR'``, ``'CRITICAL'``, or ``'NOTSET'``.

    *   Except for properties and the ``__init__`` and ``config`` methods, all
        public methods of this class (and similarly of
        :ref:`LoggingConfigDictEx`) return ``self``, to allow chaining.

    *   The (leaf) values in logging config dicts are almost all strings. The
        exceptions are ``bool`` values and actual streams allowed as the value
        of ``'stream'`` in a handler subdictionary (e.g. ``stream=sys.stdout``).
        This package uses ``bool`` values, but not actual streams, preferring
        the text equivalents accepted by the `logging` module's ``configDict()``
        method:

            instead of ``stream=sys.stdout``,
            we use ``stream='ext://sys.stdout'``.

        The reason: the ``clone_handler()`` method of the subclass
        ``LoggingConfigDictEx`` uses ``deepcopy()``, and streams can't be
        deep-copied. We recommend that you not use actual streams, but rather
        the text equivalents, as shown in the example just given.

    |hr|
    """
    _level_names = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NOTSET')

    def __init__(self,      # *,
                 root_level='WARNING',              # == logging default
                 disable_existing_loggers=None      # logging default: True
                ):
        """
        :param root_level: a ``str`` name of a loglevel.
        :param disable_existing_loggers: corresponds to
            the ``logging.config.dictConfig()`` keyword parameter of the
            same name. Using the default value ``None`` causes the `logging`
            module's default value ``True`` to be used.
        """
        assert root_level in self._level_names
        super(LoggingConfigDict, self).__init__()
        self['version'] = 1
        # self['disable_existing_loggers'] = True
        self['formatters'] = {}
        self['filters'] = {}
        self['handlers'] = {}
        self['loggers'] = {}
        self['root'] = dict(level=root_level,
                            handlers=[])
        # Note: though it sounds promising, 'incremental' is not very useful.
        # From the logging.config docs:
        # "because objects such as filters and formatters are anonymous, once
        #  a configuration is set up, it is not possible to refer to such
        #  anonymous objects when augmenting a configuration."
        # That is, ``dictConfig`` doesn't retain the names used for formatters,
        # filters and handlers in the logging config dict it processes.
        self['incremental'] = False         # logging default value

        # self['disable_existing_loggers'] can also be set
        #  with .config(disable_existing_loggers=flag)
        if disable_existing_loggers is not None:
            self['disable_existing_loggers'] = bool(disable_existing_loggers)

    # notational conveniences
    @property
    def formatters(self):
        """(Property) Return the ``'formatters'`` subdictionary, which maps
        each formatter name to the corresponding (sub)subdictionary."""
        return self['formatters']

    @property
    def filters(self):
        """(Property) Return the ``'filters'`` subdictionary, which maps
        each filter name to the corresponding (sub)subdictionary."""
        return self['filters']

    @property
    def handlers(self):
        """(Property) Return the ``'handlers'`` subdictionary, which maps
        each handler name to the corresponding (sub)subdictionary.
        """
        return self['handlers']

    @property
    def loggers(self):
        """(Property) Return the ``'loggers'`` subdictionary, which maps
        each nonempty logger name to the corresponding (sub)subdictionary."""
        return self['loggers']

    @property
    def root(self):
        """(Property) Return the ``'root'`` subdictionary."""
        return self['root']

    # TODO docstring: add links to Py docs for
    #  |   ``Formatter.__init__``
    #  |   logging config, formatters (which doesn't mention 'style')

    def add_formatter(self, formatter_name,     # *,
                      class_='logging.Formatter',   # the typical case
                      format=None,
                      dateformat=None,
                      style='%',
                      ** format_dict):
        """Add a formatter to the ``'formatters'`` subdictionary.

        :param formatter_name: just that

        Other explicit keyword parameters correspond to the  parameters used by
        ``Formatter.__init__`` and by ``dictConfig``, offering improvings
        to those different and inconsistent names. You can still use
        ``datefmt``, but you can also use ``fmt`` and ``dateformat``.

        :param format: the format string. ``Formatter.__init__`` calls this
            ``fmt``. This method recognizes ``fmt`` too, as a synonym;
            "format" takes precedence over "fmt" if both are given.

        :param dateformat; a format string for dates and times, Both
            ``Formatter.__init__`` and ``dictConfig`` call this ``datefmt``,
            for which ``dateformat`` is a synonym. In this case,
            "datefmt" takes precedence over "dateformat" if both are given.

        :param style: One of '%', '{' or '$' to specify the formatting style
            used by the format string.

        :param format_dict: Any other key/value pairs (for custom
            subclasses, perhaps)

        :return: ``self``
        """
        assert 'class' not in format_dict
        assert 'class_' not in format_dict
        format_dict['class'] = class_

        # . v0.7.7b7
        # "fmt" is recognized too;
        # "format" takes precedence over "fmt" if both are given
        format_dict['format'] = format or format_dict.get('fmt', None)

        # However, "datefmt" takes precedence over "dateformat" if both are given
        dfmt = format_dict.get('datefmt', None) or dateformat
        if dfmt:
            format_dict['datefmt'] = dfmt
        if style != '%':
            format_dict['style'] = style

        self.formatters[formatter_name] = format_dict.copy()
        return self

    def add_filter(self, filter_name,
                   ** filter_dict):
        """Add a filter to the ``'filters'`` subdictionary.

        :param filter_name: just that
        :param filter_dict: keyword/value pairs (values are generally strings)
        :return: ``self``
        """
        # assert 'class' not in filter_dict
        # if 'class_' in filter_dict:
        #     filter_dict['class'] = filter_dict.pop('class_')
        ## Todo: does this even work? logging docs kinda stink re filters.
        ## We can add a filter as in test_filters_on_logger in tests/test_LoggingConfigDict.py
        ##      ** {'()': lambda: _count_debug }
        ## and
        ##    ** {'()': CountInfo
        ## but 'class_' doesn't do the right thing, nor does 'name' (see logging source)
        ## SO the hell with it.

        self.filters[filter_name] = filter_dict.copy()
        return self

    @staticmethod
    def _to_seq(str_or_seq):
        """Utility function that lets methods allow parameters to be either
        a name or a sequence of names. Return a list of names.
        :param str_or_seq: a name of a thing (filter, handler),
                            or a sequence of names of homogeneous things,
                            or None.
        :return: sequence of names. If ``str_or_seq`` is a ``str``,
            return ``[str_or_seq]``; if ``str_or_seq`` is ``None``,
            return ``[]``; otherwise, return ``str_or_seq``.
        """
        if isinstance(str_or_seq, str):
            str_or_seq = [str_or_seq]
        return list(str_or_seq or [])

    def add_handler(self, handler_name,     # *,
                    filters=None,
                    ** handler_dict):
        """Add a handler to the ``'handlers'`` subdictionary.

        :param handler_name: just that
        :param formatter: name of a previously added formatter
        :param filters: the name of a filter, or a sequence of names of filters,
            to be used by the handler
        :param ** handler_dict: keyword/value pairs (values are generally
            strings). For the special keyword ``class``, use ``class_``.
        :return: ``self``
        """
        assert 'class' not in handler_dict
        if 'class_' in handler_dict:
            handler_dict['class'] = handler_dict.pop('class_')

        filters = self._to_seq(filters)
        if filters:
            handler_dict['filters'] = filters

        self.handlers[handler_name] = handler_dict.copy()
        return self

    # << TODO >> What is logging default? It's 'a', isn't it.
    # << TODO >> mode='w' ---- DOCUMENT: differs from logging default ('a')
    # << TODO >> Change this to mode='a' ???  That may well be what people
    #      |     want for production. It makes testing a nuisance --
    #      |     anyway, we'd have to add explicit mode='w' to (almost?) all
    #      |     file handlers used in tests.
    #      |     [and what about examples?]
    def add_file_handler(self, handler_name,    # *,
                         filename,
                         formatter,
                         mode='w',
                         level='NOTSET',    # log everything: `logging` default
                         delay=False,
                         **kwargs):
        """Add a handler with the given name, of class
        ``'logging.FileHandler'``, using the filename, formatter, and other data
        provided.

        :param handler_name: just that
        :param filename: The name of the file to which this handler should log
            messages. It may contain an absolute or relative path, as well.
        :param formatter: The name of a previously added formatter, to be used
            by this handler.
        :param mode: The mode for writing.
        :param level: The loglevel of this file handler.
        :param delay: If True, the file will be created lazily, only when
            actually written to.
        :param kwargs: Any other key/value pairs to pass to ``add_handler()``.
        :return: ``self``
        """
        self.add_handler(handler_name,
                         class_='logging.FileHandler',
                         filename=filename,
                         formatter=formatter,
                         mode=mode,
                         level=level,
                         delay=delay,
                         **kwargs)
        return self

    def attach_handler_filters(self, handler_name, * filter_names):
        """
        Add filters in ``filter_names`` to the handler named ``handler_name``.

        :param handler_name: (``str``) name of handler to attach filters to
        :param filter_names: sequence of filter names
        :return: ``self``
        """
        if not filter_names:
            return self

        handler_dict = self.handlers[handler_name]
        handler_filters_list = handler_dict.setdefault('filters', [])
        handler_filters_list.extend(filter_names)
        return self

    def set_handler_level(self, handler_name, level):
        """Set the loglevel of handler `handler_name`.
        Raise KeyError if no such handler.

        :param handler_name: name of handler.
        :param level: loglevel (as ``str``)
        :return: ``self``
        """
        assert level in self._level_names
        self.handlers[handler_name]['level'] = level
        return self

    def attach_root_handlers(self, * handler_names):
        """Add handlers in ``handler_names`` to the root logger.

        :return: ``self``
        """
        self.root['handlers'].extend(handler_names)
        return self

    def attach_root_filters(self, * filter_names):
        """Add filters in ``filter_names`` to the root logger.

        :return: ``self``
        """
        if not filter_names:
            return self
        root_filters_list = self.root.setdefault('filters', [])
        root_filters_list.extend(filter_names)
        return self

    def set_root_level(self, root_level):
        """
        Set the loglevel of the root handler.
        Given that ``__init__`` has a ``root_level`` parameter, this isn't
        really needed.

        :param root_level: an explicit value. The default set in ``__init__``
            is ``'WARNING'``.
        :return: ``self``
        """
        assert root_level in self._level_names
        self.root['level'] = root_level
        return self

    def add_logger(self,
                   logger_name,     # *,
                   handlers=None,
                   level='NOTSET',
                   propagate=None,
                   filters=None):
        """Add a logger to the ``'loggers'`` subdictionary.

        :param logger_name: just that
        :param handlers: a handler name, or sequence of handler names
        :param level: a logging level (as ``str``)
        :param propagate: (bool) whether to propagate to parent logger(s).
                The default ``None`` causes the `logging` module's default
                value of ``True`` to be used.
        :param filters: a filter name, or sequence of filter names
        :return: ``self``
        """
        d = {'level': level}

        handlers = self._to_seq(handlers)
        if handlers:
            d['handlers'] = handlers

        if propagate is not None:
            d['propagate'] = propagate

        filters = self._to_seq(filters)
        if filters:
            d['filters'] = filters

        self.loggers[logger_name] = d
        return self

    # By analogy with the attach_root_*s methods:

    def attach_logger_handlers(self, logger_name, * handler_names):
        """
        Add handlers in ``handler_names`` to the logger named ``logger_name``.

        :param logger_name: (``str``) name of logger to attach handlers to
        :param handler_names: sequence of handler names
        :return: ``self``
        """
        if not logger_name:
            self.attach_root_handlers(* handler_names)
        elif handler_names:
            logger_handlers_list = self.loggers[logger_name].setdefault(
                                                                'handlers', [])
            logger_handlers_list.extend(handler_names)
        return self

    def attach_logger_filters(self, logger_name, * filter_names):
        """Add filters in ``filter_names`` to the logger named ``logger_name``.

        :param logger_name: (``str``) name of logger to attach filters to
        :param filter_names: sequence of filter names
        :return: ``self``
        """
        if not filter_names:
            return self

        if not logger_name:
            self.attach_root_filters(* filter_names)
        else:
            logger_dict = self.loggers[logger_name]
            logger_filters_list = logger_dict.setdefault('filters', [])
            logger_filters_list.extend(filter_names)

        return self

    def set_logger_level(self, logger_name,     # *,
                         level):
        """If ``logger_name`` is empty, set the loglevel of the root handler to
        ``level``, else set the loglevel of handler ``logger_name`` to
        ``level``.

        Raise ``KeyError`` if no such logger.

        :return: ``self``
        """
        assert level in self._level_names

        if not logger_name:
            self.set_root_level(level)
        else:
            self.loggers[logger_name]['level'] = level
        return self

    def config(self,    # *,
               disable_existing_loggers=None):
        """Call ``logging.config.dictConfig()`` with the dict we've built.

        :param disable_existing_loggers: Last chance to change this setting.

        By default, LoggingConfigDicts are created with

            ``self['disable_existing_loggers'] == False``

        The ``logging`` module defaults this setting to ``True``.
        """
        if disable_existing_loggers is not None:
            self['disable_existing_loggers'] = bool(disable_existing_loggers)
        logging.config.dictConfig(dict(self))

    def dump(self):                                     # pragma: no cover
        """Pretty-print the underlying ``dict``.
        For debugging, sanity checks, etc.

        :return: ``self`` (even this)
        """
        from pprint import pformat
        print(  '---->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
              + pformat(dict(self)) + '\n'
              + '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<.'     #, flush=True
        )
        return self

    # TODO: Or, make this a global function?
    def check(self, verbose=True):
        """Check for consistency: names used to refer to entities (formatters,
        handlers, filters) must exist (must actually have been added).

        :param verbose: If true, write details of all problems to ``stderr``.
        :return: ``self`` if self is consistent.

        Raises ``KeyError`` (?) if ``self`` is not consistent.
        """
        from collections import namedtuple
        Problem = namedtuple("Problem",
                             "owner_kind, owner_name, owned_kind, bad_name")
        problems = []   # type: list[Problem]

        filters_ = self.filters
        handlers_ = self.handlers

        # HANDLERS -- formatter, filters

        formatters_ = self.formatters

        for hname in handlers_:
            hdict = handlers_[hname]    # type: dict
            # ensure any/all formatters on hname exists in formatters_
            hform_name = hdict.get('formatter', None)
            if hform_name not in formatters_:
                problems.append(
                    Problem('handler', hname, 'formatter', hform_name)
                )

            # ensure any/all filters on hname all exist (in filters_)
            hfilters = hdict.get('filters', [])
            for hfilt_name in hfilters:
                if hfilt_name not in filters_:
                    problems.append(
                        Problem('handler', hname, 'filter', hfilt_name)
                    )

        # LOGGERS -- filters, handlers

        loggers_ = self.loggers

        for lname in loggers_:
            ldict = loggers_[lname]
            # if ldict has filters   (has a 'filters' key)
            #    ensure they all exist in filters_
            lfilters = ldict.get('filters', [])
            for lfilt_name in lfilters:
                if lfilt_name not in filters_:
                    problems.append(
                        Problem('logger', lname, 'filter', lfilt_name)
                    )

            # ldict may or may not have a 'handlers' key.
            lhandlers = ldict.get('handlers', [])
            # ensure that every handler lhname in lhandlers exists in handlers_
            for lhname in lhandlers:
                if lhname not in handlers_:
                    problems.append(
                        Problem('logger', lname, 'handler', lhname)
                    )

        # ROOT logger -- filters, handlers

        root_ = self.root

        # if root_ has filters, ensure they all exist in filters_
        rfilters = root_.get('filters', [])
        for rfilt_name in rfilters:
            if rfilt_name not in filters_:
                problems.append(
                    Problem('logger', '', 'filter', rfilt_name)
                )

        # Assume root_ has a 'handlers' key.
        # for every handler hn in root_['handlers']
        #    ensure hn exists // in handlers_
        rhandlers = root_['handlers']
        for rhname in rhandlers:
            if rhname not in handlers_:
                problems.append(
                    Problem('logger', '', 'handler', rhname)
                )

        # ------------------------------

        def print_err(msg, **kwargs):
            import sys
            if PY2:
                msg = unicode(msg)
            print(msg, file=sys.stderr, **kwargs)

        if problems:
            if verbose:
                print_err("Problems -- nonexistent things mentioned")
                for prob in problems:
                    print_err(
                        "%(owner_kind)10s %(owner_name)15r "
                        "mentions %(owned_kind)10s %(bad_name)r"
                        % prob._asdict()
                    )
            raise KeyError("names used that correspond to no added entities")

        # ------------------------------

        return self
