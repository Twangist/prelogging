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

    _warn = False

    @classmethod
    def warn(cls, warn_val=None):
        """Get or set the bool value of the class attribute ``_warn``. When
        true, ``LoggingConfigDict`` will write warnings when

            * an entity (formatter, filter, etc.) is added that has already
              been defined, possibly overwriting the existing definition;
            * attaching a formatter to a handler replaces the handler's
              existing, different formatter
            * attaching a formatter to a handler that it's already attached to
            * attaching a {filter/handler} to a {handler/logger} that it's
              already attached to.

        :param warn_val: If not ``None``, set ``cls._warn`` to ``bool(warn_val)``.
        type warn_val: bool or None
        :return: ``cls._warn`` (== ``warn_val`` if that is not ``None``)
        """
        if warn_val is not None:
            cls._warn = bool(warn_val)
        return cls._warn

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

    def add_formatter(self, formatter_name,     # *,
                      class_='logging.Formatter',   # the typical case
                      format=None,
                      dateformat=None,
                      style='%',            # Only '%' works in Py2
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

        :param style: (*Python 3 only*) One of '%', '{' or '$' to specify the
            formatting style used by the format string.

        :param format_dict: Any other key/value pairs (for custom
            subclasses, perhaps)

        :return: ``self``
        """
        self._check_readd(self.formatters, formatter_name, 'formatter')

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
        :param filter_dict: keyword/value pairs
            The value of the key '()' is a callable that returns
            the Filter class or callable filter;
            other key/value pairs are arguments for this callable
            (used once, to construct/initialize the filter).
        :return: ``self``
        """
        self._check_readd(self.filters, filter_name, 'filter')
        self.filters[filter_name] = filter_dict     #.copy()      <---- TODO?
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
                    formatter=None,
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
        self._check_readd(self.handlers, handler_name, 'handler')

        assert 'class' not in handler_dict
        if 'class_' in handler_dict:
            handler_dict['class'] = handler_dict.pop('class_')

        if formatter:
            handler_dict['formatter'] = formatter

        filters = self._to_seq(filters)
        filters = self._check_attach__clean_list(
            existing_attachees=None,
            attach_to=handler_name,
            attach_to_kind='handler',
            attachees=filters,
            attachee_kind='filter'
        )
        if filters:
            handler_dict['filters'] = filters

        self.handlers[handler_name] = handler_dict  #.copy()    <---- TODO?
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

    def add_null_handler(self,
                         handler_name,  # *
                         level='NOTSET',
                         **kwargs):
        """Add a ``logging.NullHandler``.

        :param handler_name: name of the handler
        :param level: the handler's loglevel
        :param kwargs: any additional key/value pairs for add_handler
            (typically none)
        :return: ``self``
        """
        return self.add_handler(
            handler_name,
            class_='logging.NullHandler',
            level=level,
            **kwargs)

    # TODO: TEST
    def attach_handler_formatter(self, handler_name, formatter_name):
        """Attach formatter to handler.
        Raise ``KeyError`` if no such handler.

        Of course you can't attach a formatter to anything other than a handler,
        so admittedly the "_handler" part of the method name is redundant. In
        its defense,

            * it's by analogy with all the other "attach_*" functions,
              which are of the form "attach_toWhat_thingsToAttach"

            * it tells you the order of parameters.

        :param handler_name: name of handler to attach formatter to
        ;param formatter_name: name of formatter
        :return: ``self``
        """
        self._check_attach_formatter(handler_name, formatter_name)

        self.handlers[handler_name]['formatter'] = formatter_name
        return self

    def attach_handler_filters(self, handler_name, * filter_names):
        """
        Add filters in ``filter_names`` to the handler named ``handler_name``.
        Raise ``KeyError`` if no such handler.

        :param handler_name: (``str``) name of handler to attach filters to
        :param filter_names: sequence of filter names
        :return: ``self``
        """
        if not filter_names:
            return self

        handler_dict = self.handlers[handler_name]
        handler_filters = handler_dict.get('filters', None)

        filter_names = self._check_attach__clean_list(
            existing_attachees=handler_filters,
            attach_to=handler_name,
            attach_to_kind='handler',
            attachees=filter_names,
            attachee_kind='filter'
        )
        if not filter_names:
            return self
        handler_filters = handler_dict.setdefault('filters', [])
        handler_filters.extend(filter_names)
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
        root_handlers = self.root['handlers']

        # check/clean duplicates from handler_names
        handler_names = self._check_attach__clean_list(
            existing_attachees=root_handlers,
            attach_to='',
            attach_to_kind='logger',
            attachees=handler_names,
            attachee_kind='handler'
        )
        root_handlers.extend(handler_names)
        return self

    def attach_root_filters(self, * filter_names):
        """Add filters in ``filter_names`` to the root logger.

        :param filter_names: (vararg) tuple of filter names
        :return: ``self``
        """
        if not filter_names:
            return self
        root_filters = self.root.get('filters', None)

        # check/clean duplicates & reattachments from filter_names
        filter_names = self._check_attach__clean_list(
            existing_attachees=root_filters,
            attach_to='',
            attach_to_kind='logger',
            attachees=filter_names,
            attachee_kind='filter'
        )
        if not filter_names:
            return self

        root_filters = self.root.setdefault('filters', [])
        root_filters.extend(filter_names)
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
        self._check_readd(self.loggers, logger_name, 'logger')
        d = {'level': level}

        handlers = self._to_seq(handlers)
        # check/clean handlers
        handlers = self._check_attach__clean_list(
            existing_attachees=None,
            attach_to=logger_name,
            attach_to_kind='logger',
            attachees=handlers,
            attachee_kind='handler'
        )
        if handlers:
            d['handlers'] = handlers

        if propagate is not None:
            d['propagate'] = propagate

        filters = self._to_seq(filters)
        # check/clean filters
        filters = self._check_attach__clean_list(
            existing_attachees=None,
            attach_to=logger_name,
            attach_to_kind='logger',
            attachees=filters,
            attachee_kind='filter'
        )
        if filters:
            d['filters'] = filters

        self.loggers[logger_name] = d
        return self

    # By analogy with the attach_root_*s methods:

    def attach_logger_handlers(self, logger_name, * handler_names):
        """
        Add handlers in ``handler_names`` to the logger named ``logger_name``.
        Raise ``KeyError`` if no such logger.

        :param logger_name: (``str``) name of logger to attach handlers to
        :param handler_names: sequence of handler names
        :return: ``self``
        """
        if not logger_name:
            return self.attach_root_handlers(* handler_names)

        if not handler_names:
            return self

        logger_handlers = self.loggers[logger_name].setdefault('handlers', [])
        handler_names = self._check_attach__clean_list(
            existing_attachees=logger_handlers,
            attach_to=logger_name,
            attach_to_kind='logger',
            attachees=handler_names,
            attachee_kind='handler'
        )
        logger_handlers.extend(handler_names)
        return self

    def attach_logger_filters(self, logger_name, * filter_names):
        """Add filters in ``filter_names`` to the logger named ``logger_name``.
        Raise ``KeyError`` if no such logger.

        :param logger_name: (``str``) name of logger to attach filters to
        :param filter_names: sequence of filter names
        :return: ``self``
        """
        if not filter_names:
            return self

        if not logger_name:
            return self.attach_root_filters(* filter_names)

        logger_dict = self.loggers[logger_name]
        logger_filters = logger_dict.get('filters', None)
        filter_names = self._check_attach__clean_list(
            existing_attachees=logger_filters,
            attach_to=logger_name,
            attach_to_kind='logger',
            attachees=filter_names,
            attachee_kind='filter'
        )
        if not filter_names:
            return self

        logger_filters = logger_dict.setdefault('filters', [])
        logger_filters.extend(filter_names)

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

        The `logging` module defaults this setting to ``True``.
        """
        if disable_existing_loggers is not None:
            self['disable_existing_loggers'] = bool(disable_existing_loggers)
        if self.warn():     # 0.2.7b13
            self.check()    # 0.2.7b13
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

    # -------------------------------------------------------
    # Consistency checking
    # -------------------------------------------------------

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

            # ensure any/all filters on hname exist in filters_
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
            # ensure that every handler in lhandlers exists in handlers_
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
        # ensure every handler in root_['handlers'] exists in handlers_
        rhandlers = root_['handlers']
        for rhname in rhandlers:
            if rhname not in handlers_:
                problems.append(
                    Problem('logger', '', 'handler', rhname)
                )

        # ------------------------------

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

    @staticmethod
    def _get_caller_srcfile_lineno(depth=3):
        """Return source file name and line number from which this function
            was called.

        :param depth: how many levels in the call stack to go "down":
            0 = this function, 1 = caller of this this function,
            2 = caller's caller, etc. For the default of 3, we return
            source file name and line number for the caller's caller's
            caller.
        :return: Tuple (srcfile, lineno) -- the source file name, and line
            number, of the caller's ... caller (depending on ``depth``).
        """
        import sys
        caller_n_frame = sys._getframe(depth)
        # frame has
        #     f_lineno    # curr line #
        #     f_code      # code obj
        # code obj has
        #     co_filename
        srcfile = caller_n_frame.f_code.co_filename
        lineno = caller_n_frame.f_lineno
        # TODO? make path of srcfile relative to current directory?
        return srcfile, lineno

    def _check_readd(self,
                     subdict, key, kind):
        """
        :param subdict: self.formatters, self.handlers, etc.
        :param key: name of formatter, handler, etc. Will be a key into subdict.
        :param kind: "formatter", "handler", etc. for use in warning message
        """
        if not self._warn:
            return
        srcfile, lineno = self._get_caller_srcfile_lineno()
        if key in subdict:
            print_err(
                "Warning (%s, line %d): redefinition of %s '%s'."
                % (srcfile, lineno, kind, key)
            )

    def _check_attach_formatter(self, handler_name, formatter_name):
        if not self._warn:
            return
        # If handler doesn't have a formatter yet, ok
        existing_fname = self.handlers[handler_name].get('formatter', None)
        if existing_fname is None:
            return

        # Two different warnings, depending on whether:
        #   * formatter_name == existing_fname, or
        #   * formatter_name != existing_fname
        srcfile, lineno = self._get_caller_srcfile_lineno()
        if formatter_name != existing_fname:
            print_err(
                "Warning (%s, line %d): formatter '%s' replaces '%s' in handler '%s'."
                % (srcfile, lineno, formatter_name, existing_fname, handler_name)
            )
        else:
            print_err(
                "Warning (%s, line %d): formatter '%s' already attached to handler '%s'."
                % (srcfile, lineno, formatter_name, handler_name)
            )

    def _check_attach__clean_list(self,     # *
            existing_attachees=None,
            attach_to=None,
            attach_to_kind=None,
            attachees=None,
            attachee_kind=None):
        """
        :param existing_attachees: list/seq
        :param attach_to: name of thing being attached to
        :param attach_to_kind: 'handler' or 'logger'
        :param attachees: list/sequence of names of things being attached
        :param attachee_kind: 'filter', 'handler'
        return: list -- attachees with duplicates removed
            and with any items removed that are in ``existing_attachees``
        """
        existing_attachees = existing_attachees or []
        # Remove duplicates, form list of them (for warning msg)
        dups = []
        cleaned = []
        for name in attachees:
            if name not in cleaned:
                cleaned.append(name)
            else:
                dups.append(name)
        # Warn if dups not empty
        if self._warn and dups:
            srcfile, lineno = self._get_caller_srcfile_lineno()
            dups_str = str(dups)[1:-1]
            print_err(
                "Warning (%s, line %d):"
                " list of %ss to attach to %s '%s' contains duplicates:"
                " %s."
                % (srcfile, lineno,
                   attachee_kind, attach_to_kind, attach_to,
                   dups_str)
            )

        # Check for reattachment, remove such
        reattached = []
        cleaned2 = []
        for name in cleaned:
            if name not in existing_attachees:
                cleaned2.append(name)
            else:
                reattached.append(name)
        # Warn if reattached not empty
        if self._warn and reattached:
            srcfile, lineno = self._get_caller_srcfile_lineno()
            reattached_str = str(reattached)[1:-1]
            print_err(
                "Warning (%s, line %d):"
                " these %ss are already attached to %s '%s':"
                " %s."
                % (srcfile, lineno,
                   attachee_kind, attach_to_kind, attach_to,
                   reattached_str)
            )

        return cleaned2


def print_err(msg, **kwargs):
    import sys
    if PY2:
        msg = unicode(msg)
    print(msg, file=sys.stderr, **kwargs)
