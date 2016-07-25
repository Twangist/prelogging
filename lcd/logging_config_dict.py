# coding=utf-8

from __future__ import print_function

__author__ = "Brian O'Neill"

__doc__ = """ \
The methods of this class —``add_formatter``, ``add_filter``,
``add_handler``, ``add_logger``, and so on — operate on the underlying dictionary.
That dict is significantly nested, and keys often appear among the data, as
back references to things "already defined".

.. _Using-a-LoggingConfigDict:

.. index:: Using a LoggingConfigDict

**Using a** ``LoggingConfigDict``  |br|
``- - - - - - - - - - - - - - - - - - - - - - - - -``

Although dicts are unordered, when configuring logging there's a precedence ordering
for specifying objects:

    1. Create a ``LoggingConfigDict``, optionally specifying the level of
       the root handler.

    2. Add formatter specifications with ``add_formatter()``.

    3. Add any filter specifications with ``add_filter()``.

    4. Add handler specifications with ``add_handler()`` and/or ``add_file_handler()``,
       referring by name to formatters and filters already specified in previous steps.

    *In steps 2. – 4. you give each thing specified a name, by which you refer to it
    in subsequent steps when associating the thing with other, higher-level things.*

    5. If desired, configure the root logger using ``attach_root_handlers()``,
       ``attach_root_filters()`` and/or ``set_root_level()``, referring by name
       to handlers and filters already specified in previous steps.

    6. Add specifications for any non-root loggers with ``add_logger()``.
       Specify the handlers and filters of a logger by name, using the ``handlers``
       and ``filters`` keyword parameters.

    *Steps 2. and 3. can be interchanged, likewise Steps 5. and 6.*

A single ``LoggingConfigDict`` can be passed around to different "areas" of a program,
each contributing specifications of its desired formatters, filters, handlers and
loggers.

Once a ``LoggingConfigDict`` has been populated, it can be used to configure
logging by calling its ``config()`` method, which is basically just shorthand
for a call to
`logging.config.dictConfig() <https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig>`_.
"""

import logging
import logging.config
from ._version import IS_PY2

class LoggingConfigDict(dict):
    """
    .. include:: _global.rst

    A general class that simplifies building a logging config dict, modularly
    and incrementally, for ultimate use with the ``config()`` method of this
    class, which simply calls
    `logging.config.dictConfig() <https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig>`_.
    The methods of ``LoggingConfigDict`` let you dispense with lots (and lots)
    of nested curly braces and single-quotes around keywords.

    *   In this class as well as in :ref:`LoggingConfigDictEx`, "level" always
        means the ``str`` name of the level, e.g. ``'DEBUG'``, not the numeric
        value ``logging.DEBUG``. A level name, in short — one of ``'DEBUG'``,
        ``'INFO'``, ``'WARNING'``, ``'ERROR'``, ``'CRITICAL'``, or ``'NOTSET'``.

    *   Except for ``config()`` and the properties ``formatters``, ``filters``,
        ``handlers``, ``loggers`` and ``root``, all public methods of this class
        and of :ref:`LoggingConfigDictEx` return ``self``, to allow chaining.

    *   The (leaf) values in logging config dicts are almost all strings. The
        exceptions are ``bool`` values and actual streams allowed as the value
        of ``'stream'`` in a handler subdictionary (e.g. ``stream=sys.stdout``).
        This package uses ``bool`` values, but not actual streams, preferring
        the text equivalents accepted by the `logging` module's ``configDict()``
        method:

            instead of ``stream=sys.stdout``, we use ``stream='ext://sys.stdout'``.

        The reason: the ``clone_handler()`` method of the subclass ``LoggingConfigDictEx``
        uses ``deepcopy()``, and streams can't be deep-copied. We recommend
        that you not use actual streams, but rather the text equivalents, as
        shown in the example just given.

    """
    _level_names = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NOTSET')

    def __init__(self,      # *,
                 root_level='WARNING',              # == logging default level
                 disable_existing_loggers=None      # logging default value is True
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

    def set_root_level(self, root_level):
        """
        Set the loglevel of the root handler.
        Given that ``__init__`` has a ``root_level`` parameter, this isn't really needed.

        :param root_level: an explicit value. The default set in ``__init__``
            is ``'WARNING'``.
        :return: ``self``
        """
        assert root_level in self._level_names
        self.root['level'] = root_level
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

    # Note, 0.2.7 By analogy, add_logger_*s methods

    def attach_logger_handlers(self, logger_name, * handler_names):
        """Add handlers in ``handler_names`` to the logger named ``logger_name``.

        :param logger_name: (``str``) name of logger to attach handlers to
        :param handler_names: sequence of handler names
        :return: ``self``
        """
        if not logger_name:
            self.attach_root_handlers(* handler_names)
        elif handler_names:
            logger_handlers_list = self.loggers[logger_name].setdefault('handlers', [])
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

    def attach_handler_filters(self, handler_name, * filter_names):
        """Add filters in ``filter_names`` to the handler named ``handler_name``.

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

    def add_formatter(self, formatter_name,     # *,
                      class_='logging.Formatter',   # the typical case
                      ** format_dict):
        """Add a formatter to the ``'formatters'`` subdictionary.

        :param formatter_name: just that
        :param ** format_dict: keyword/value pairs (values are generally strings)
                    For the special keyword `class`, which is a Python reserved word
                    and therefore can't be used as a keyword parameter, use `class_`.
        :return: ``self``
        """
        assert 'class' not in format_dict
        assert 'class_' not in format_dict
        format_dict['class'] = class_
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
        """Utility function that lets methods allow parameters to be either a name
         or a sequence of names. Return a list of names.
        :param str_or_seq: a name of a thing (filter, handler),
                            or a sequence of names of homogeneous things,
                            or None.
        :return: sequence of names. If ``str_or_seq`` is a ``str``,
            return ``[str_or_seq]``; if ``str_or_seq`` is ``None``, return ``[]``;
            otherwise, return ``str_or_seq``.
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
        :param ** handler_dict: keyword/value pairs (values are generally strings)
            For the special keyword ``class``, use ``class_``.
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

    def add_file_handler(self, handler_name,    # *,
                         filename,
                         formatter,     # ='process_logger_level_msg'
                         mode='w',
                         level='NOTSET',    # log everything: logging module default
                         delay=False,
                         **kwargs):
        """Add a handler with the given name, with class ``'logging.FileHandler'``,
        using the filename, formatter, and other data provided.

        :param handler_name: just that
        :param filename: The name of the file to which this handler should log messages.
            It may contain an absolute or relative path, as well.
        :param formatter: The name of a previously added formatter, to be used
            by this handler.
        :param mode: The mode for writing.
        :param level: The loglevel of this file handler.
        :param delay: If True, the file will be created lazily, only when actually
            written to.
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

    def set_logger_level(self, logger_name,     # *,
                         level):
        """If ``logger_name`` is empty, set the loglevel of the root handler to
        ``level``, else set the loglevel of handler ``logger_name`` to ``level``.

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
        handlers, filters) must exist/must actually have been added.

        :param verbose: If true, write details of all problems to ``stderr``.
        :return: ``self`` if self is consistent.

        Raises ``KeyError`` (?) if self is not consistent.
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
            # make sure any/all formatters on hname exists in formatters_
            hform_name = hdict.get('formatter', None)
            if hform_name not in formatters_:
                problems.append(
                    Problem('handler', hname, 'formatter', hform_name)
                )

            # make sure any/all filters on hname all exist (in filters_)
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
            #    make sure they all exist in filters_
            lfilters = ldict.get('filters', [])
            for lfilt_name in lfilters:
                if lfilt_name not in filters_:
                    problems.append(
                        Problem('logger', lname, 'filter', lfilt_name)
                    )

            # ldict may or may not have a 'handlers' key.
            lhandlers = ldict.get('handlers', [])
            # make sure that every handler lhname in lhandlers exists in handlers_
            for lhname in lhandlers:
                if lhname not in handlers_:
                    problems.append(
                        Problem('logger', lname, 'handler', lhname)
                    )

        # ROOT logger -- filters, handlers

        root_ = self.root

        # if root_ has filters, make sure they all exist in filters_
        rfilters = root_.get('filters', [])
        for rfilt_name in rfilters:
            if rfilt_name not in filters_:
                problems.append(
                    Problem('logger', '', 'filter', rfilt_name)
                )

        # Assume root_ has a 'handlers' key.
        # for every handler hn in root_['handlers']
        #    make sure hn exists // in handlers_
        rhandlers = root_['handlers']
        for rhname in rhandlers:
            if rhname not in handlers_:
                problems.append(
                    Problem('logger', '', 'handler', rhname)
                )

        # ------------------------------

        def print_err(msg, **kwargs):
            import sys
            if IS_PY2:
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
            raise KeyError("names were used for which no such entities were added")

        # ------------------------------

        return self
