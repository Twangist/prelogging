# coding=utf-8

from __future__ import print_function
from .six import iteritems, PY2
import logging
import logging.config

__author__ = "Brian O'Neill"

__doc__ = """ \
.. _lcdictbasic-module-docstring:

``LCDictBasic`` provides an API for building dictionaries that specify
Python logging configuration -- *logging config dicts*.

Entering a logging config dict as static data requires many curly
braces, colons, single-quoted keywords, and boilerplate default key/value pairs.
Such dicts are significantly nested, and keys often appear among
the data, as back-references to things "already defined".

But logging configuration involves a small hierarchy of only four kinds of
entities — formatters, handlers, loggers and, optionally, filters —
which can be specified in a layered way.

``LCDictBasic`` lets you build a logging config dict modularly and
incrementally. It flattens the process of specifying the dict, letting you
define each entity one by one, instead of entering a thicket of nested dicts.

An ``LCDictBasic`` instance *is* a logging config dict. It inherits from
``dict``, and its methods —``add_formatter``, ``add_handler``, ``add_logger``,
and so on — operate on the underlying dictionary, breaking down the process
of creating a logging config dict into basic steps:

    1. Create an ``LCDictBasic``, optionally specifying the level of
       the root handler.

    2. Add formatter specifications with ``add_formatter()``.

    3. Add any filter specifications with ``add_filter()``.

    4. Add handler specifications with ``add_handler()`` and/or
       ``add_file_handler()``: for each filter, specify its name, formatter,
       and loglevel, and and optionally attach filters. Formatters and filters
       are specified by name, so they should already have been added in previous
       steps (if they weren't, by default `prelogging` will issue a warning). Although
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

Once you've built an ``LCDictBasic`` meeting your requirements, you
configure logging by calling the object's ``config`` method, which
passes itself (as a dict) to
`logging.config.dictConfig() <https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig>`_.
"""


class LCDictBasic(dict):
    """
    .. include:: _global.rst

    *   In this class as well as in :ref:`LCDict`, "level" always
        means the ``str`` name of the level, e.g. ``'DEBUG'``, not the numeric
        value ``logging.DEBUG``. A level name, in short — one of ``'DEBUG'``,
        ``'INFO'``, ``'WARNING'``, ``'ERROR'``, ``'CRITICAL'``, or ``'NOTSET'``.

    *   Except for properties and the ``__init__``, ``config`` and ``dump``
        methods, all public methods of this class (and similarly of
        :ref:`LCDict`) return ``self``, to allow chaining.

    *   The (leaf) values in logging config dicts are almost all strings. The
        exceptions are ``bool`` values, filters, and actual streams allowed as
        values of ``'stream'`` in a handler subdictionary (e.g. ``stream=sys.stdout``).
        This package uses ``bool`` values, but not actual streams, preferring
        the text equivalents accepted by the `logging` module's ``configDict()``
        method:

            instead of ``stream=sys.stdout``,
            we use ``stream='ext://sys.stdout'``.

        The reason: the ``clone_handler()`` method of the subclass
        ``LCDict`` uses ``deepcopy()``, and streams can't be
        deep-copied. We recommend that you not use actual streams,
        nor in general binary objects that can't be pickled,
        preferring instead their text equivalents, as shown in the example
        just given. More about the use of ``'ext://'`` (and ``'cfg://'`` can be
        found in the documentation for `logging.config`, especially
        `here <https://docs.python.org/3/library/logging.config.html#access-to-external-objects>`_.

    |hr|
    """
    _level_names = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NOTSET')

    class Warnings():
        """
        .. _warning-class:

        "Bit" values combined into the _warnings attribute of an LCDictBasic.
        Each determines whether warnings are written to stderr for a particular
        questionable practice:

        +----------------------+--------+------------------------------------------+
        || Warnings "constant" || Value || Issue a warning when...                 |
        +======================+========+==========================================+
        || REATTACH            ||   1   || attaching a {formatter/filter/handler}  |
        ||                     ||       || to a {handler/logger} that it's already |
        ||                     ||       || attached to                             |
        || REDEFINE            ||   2   || overwriting an existing definition of   |
        ||                     ||       || an entity (formatter, filter, etc.)     |
        || ATTACH_UNDEFINED    ||   4   || attaching a {formatter/filter/handler}  |
        ||                     ||       || that hasn't yet been added (defined)    |
        || REPLACE_FORMATTER   ||   8   || changing a handler's formatter          |
        +----------------------+--------+------------------------------------------+

        The default value is

            ``DEFAULT = REATTACH + REDEFINE + ATTACH_UNDEFINED``.
        """
        NONE = 0
        REATTACH            = 0b0001
        REDEFINE            = 0b0010
        ATTACH_UNDEFINED    = 0b0100
        REPLACE_FORMATTER   = 0b1000

        DEFAULT = REATTACH + REDEFINE + ATTACH_UNDEFINED
        ALL     = REATTACH + REDEFINE + ATTACH_UNDEFINED + REPLACE_FORMATTER


    def __init__(self,      # *,
                 root_level='WARNING',              # == logging default
                 disable_existing_loggers=None,     # logging default: True
                 warnings=Warnings.DEFAULT
                ):
        """
        :param root_level: a ``str`` name of a loglevel.
        :param disable_existing_loggers: corresponds to
            the ``logging.config.dictConfig()`` keyword parameter of the
            same name. Using the default value ``None`` causes the `logging`
            module's default value ``True`` to be used.
        :param warnings: A bit field, a combination of values defined in
            the inner class `LCDictBasic.Warnings``. The default value is
            ``REATTACH + REDEFINE + ATTACH_UNDEFINED``.

            This value is saved; it can be read and written with the ``warnings``
            property.
        """

        assert root_level in self._level_names
        super(LCDictBasic, self).__init__()
        self['version'] = 1
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

        self._warnings = warnings

    @property
    def warnings(self):
        """Read/write property (bits, packed flags), set by ``__init__`` from
        its ``warnings`` parameter.
        """
        return self._warnings

    @warnings.setter
    def warnings(self, warnings_val):
        """Read/write property (bits, packed flags), set by ``__init__`` from
        its ``warnings`` parameter.
        """
        self._warnings = warnings_val

    @property
    def _warn_reattach(self):
        return self._warnings & self.Warnings.REATTACH

    @property
    def _warn_redefine(self):
        return self._warnings & self.Warnings.REDEFINE

    @property
    def _warn_replace_formatter(self):
        return self._warnings & self.Warnings.REPLACE_FORMATTER

    @property
    def _warn_undefined(self):
        return self._warnings & self.Warnings.ATTACH_UNDEFINED

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
                      style='%',
                      ** format_dict):
        """\
        .. _LCDB_add_formatter-docstring:

        Add a formatter to the ``formatters`` subdictionary.

        :param formatter_name: just that

        :param format: the format string. ``Formatter.__init__`` calls this
            ``fmt``; static configuration calls it ``format``. This method
            recognizes ``fmt`` too, as a synonym; "format" takes precedence over
            "fmt" if both are given.

            The `logging` module supports a large number of keywords
            that can appear in format strings — for a complete list, see
            the documentation for
            `LogRecord attributes <https://docs.python.org/3/library/logging.html?highlight=logging#logrecord-attributes>`_.
            Each logged message can even include the name of the function,
            and/or the line number, where its originating logging call was issued.

        :param dateformat: a format string for dates and times, with the same
            keys accepted by `time.strftime <https://docs.python.org/3/library/time.html#time.strftime>`_.
            Both ``Formatter.__init__`` and ``dictConfig`` call this ``datefmt``,
            for which ``dateformat`` is a synonym. In this case,
            "datefmt" takes precedence over "dateformat" if both are given.

        :param style: (*Python 3 only*)
            Although the documentation for logging configuration doesn't mention
            it, under Python 3 ``style`` also works in logging config dicts.

            ``style`` can be one of '%', '{' or '$', specifying the
            formatting style used by the format string. These possible values
            have the following significance:

            |    ``'%'``     old-style, ``%``-based formatting (the default)
            |    ``'{'``     new-style formatting, using ``str.format``
            |    ``'$'``     template-based formatting

        :param format_dict: Any other key/value pairs (for a custom
            subclasses, perhaps)

        :return: ``self``
        """
        self._check_readd(self.formatters, formatter_name, 'formatter')

        assert 'class' not in format_dict
        assert 'class_' not in format_dict
        format_dict['class'] = class_

        # "fmt" is recognized too;
        # "format" takes precedence over "fmt" if both are given
        format_dict['format'] = format or format_dict.get('fmt', None)

        # but "datefmt" takes precedence over "dateformat" if both are given
        dfmt = format_dict.get('datefmt', None) or dateformat
        if dfmt:
            format_dict['datefmt'] = dfmt
        if style != '%':
            format_dict['style'] = style

        self.formatters[formatter_name] = format_dict.copy()
        return self

    def add_filter(self, filter_name,
                   ** filter_dict):
        """Add a filter to the ``filters`` subdictionary.

        :param filter_name: just that
        :param filter_dict: keyword/value pairs
            The value of the key '()' is a callable that returns
            the Filter class or callable filter;
            other key/value pairs are arguments for this callable.
        :return: ``self``
        """
        self._check_readd(self.filters, filter_name, 'filter')
        self.filters[filter_name] = filter_dict
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
                    level='NOTSET',
                    formatter=None,
                    filters=None,
                    ** handler_dict):
        """Add a handler to the ``handlers`` subdictionary.

        :param handler_name: just that
        :param level: the loglevel of this handler (default: 'NOTSET')
        :param formatter: name of a previously added formatter
        :param filters: the name of a filter, or a sequence of names of filters,
            to be used by the handler
        :param handler_dict: keyword/value pairs (values are generally
            strings). For the special keyword ``class``, use ``class_``.
        :return: ``self``
        """
        self._check_readd(self.handlers, handler_name, 'handler')

        # assert 'class' not in handler_dict
        if 'class_' in handler_dict:
            handler_dict['class'] = handler_dict.pop('class_')

        if level != 'NOTSET':               # v0.3.1: add only if not NOTSET
            handler_dict['level'] = level
        # A little preprocessing, inspired by 'encoding=None':
        # discard items in handler_dict with value None
        handler_dict = {k: v for k, v in iteritems(handler_dict)
                        if v is not None}

        if formatter:
            self._check_defined(
                defined=self.formatters,
                attach_to=handler_name,
                attach_to_kind='handler',
                attachees=[formatter],
                attachee_kind='formatter')
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
            self._check_defined(
                defined=self.filters,
                attach_to=handler_name,
                attach_to_kind='handler',
                attachees=filters,
                attachee_kind='filter')
            handler_dict['filters'] = filters

        self.handlers[handler_name] = handler_dict
        return self

    def add_stream_handler(self, handler_name,    # *,
                           stream,
                           class_='logging.StreamHandler',
                           level='NOTSET',      # logging default
                           formatter=None,
                           **kwargs):
        """
        :param handler_name:
        :param stream: e.g. 'ext://sys.stderr' or sys.stderr
        :param formatter: the name of a formatter
        :param level: the stream handler's loglevel
        :param kwargs: any additional keyword arguments
        :return: ``self``
        """
        kwargs['class'] = class_

        if formatter is not None:
            kwargs['formatter'] = formatter

        self.add_handler(handler_name,
                         stream=stream,
                         level=level,
                         ** kwargs)
        return self

    def add_file_handler(self, handler_name,    # *,
                         filename,
                         formatter=None,
                         # mode='w',
                         mode='a',
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

    def add_null_handler(self, handler_name,  # *
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

    def set_handler_formatter(self, handler_name, formatter_name):
        """Attach formatter to handler.
        Raise ``KeyError`` if no such handler.

        Of course you can't "set" the formatter of anything other than a handler,
        so admittedly the "_handler" part of the method name is redundant. In
        its defense, the name does tell you the order of parameters.

        :param handler_name: name of handler to attach formatter to
        :param formatter_name: name of formatter
        :return: ``self``
        """
        self._check_set_formatter(handler_name, formatter_name)
        self._check_defined(
            defined=self.formatters,
            attach_to=handler_name,
            attach_to_kind='handler',
            attachees=[formatter_name],
            attachee_kind='formatter')

        self.handlers[handler_name]['formatter'] = formatter_name
        return self

    def attach_handler_filters(self, handler_name, * filter_names):
        """
        Add filters in ``filter_names`` to the handler named ``handler_name``.
        Raise ``KeyError`` if no such handler.

        :param handler_name: (``str``) name of handler to attach filters to
        :param filter_names: (vararg) zero or more  of filter names
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
        self._check_defined(
            defined=self.filters,
            attach_to=handler_name,
            attach_to_kind='handler',
            attachees=filter_names,
            attachee_kind='filter')
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
        """Attach handlers in ``handler_names`` to the root logger.

        :param handler_names: (vararg) zero or more  handler names
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
        self._check_defined(
            defined=self.handlers,
            attach_to='',
            attach_to_kind='logger',
            attachees=handler_names,
            attachee_kind='handler')
        root_handlers.extend(handler_names)
        return self

    def attach_root_filters(self, * filter_names):
        """Attach filters in ``filter_names`` to the root logger.

        :param filter_names: (vararg) zero or more  filter names
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
        self._check_defined(
            defined=self.filters,
            attach_to='',
            attach_to_kind='logger',
            attachees=filter_names,
            attachee_kind='filter')

        root_filters = self.root.setdefault('filters', [])
        root_filters.extend(filter_names)
        return self

    def set_root_level(self, level):
        """
        Set the loglevel of the root handler.
        Given that ``__init__`` has a ``level`` parameter, this isn't
        really needed.

        :param level: an explicit value. The default set in ``__init__``
            is ``'WARNING'`` (same as the `logging` default).
        :return: ``self``
        """
        assert level in self._level_names
        self.root['level'] = level
        return self

    def add_logger(self, logger_name,     # *,
                   handlers=None,
                   level='NOTSET',
                   propagate=None,
                   filters=None):
        """Add a logger to the ``loggers`` subdictionary.

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
            self._check_defined(
                defined=self.handlers,
                attach_to=logger_name,
                attach_to_kind='logger',
                attachees=handlers,
                attachee_kind='handler')
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
            self._check_defined(
                defined=self.filters,
                attach_to=logger_name,
                attach_to_kind='logger',
                attachees=filters,
                attachee_kind='filter')
            d['filters'] = filters

        self.loggers[logger_name] = d
        return self

    # By analogy with the attach_root_*s methods:

    def attach_logger_handlers(self, logger_name, * handler_names):
        """
        Add handlers in ``handler_names`` to the logger named ``logger_name``.
        Raise ``KeyError`` if no such logger.

        :param logger_name: (``str``) name of logger to attach handlers to
        :param handler_names: (vararg) zero or more  handler names
        :return: ``self``
        """
        if not logger_name:
            return self.attach_root_handlers(* handler_names)

        logger_handlers = self.loggers[logger_name].setdefault('handlers', [])
        handler_names = self._check_attach__clean_list(
            existing_attachees=logger_handlers,
            attach_to=logger_name,
            attach_to_kind='logger',
            attachees=handler_names,
            attachee_kind='handler'
        )
        self._check_defined(
            defined=self.handlers,
            attach_to=logger_name,
            attach_to_kind='logger',
            attachees=handler_names,
            attachee_kind='handler')
        logger_handlers.extend(handler_names)
        return self

    def attach_logger_filters(self, logger_name, * filter_names):
        """Add filters in ``filter_names`` to the logger named ``logger_name``.
        Raise ``KeyError`` if no such logger.

        :param logger_name: (``str``) name of logger to attach filters to
        :param filter_names: (vararg) zero or more  filter names
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
        self._check_defined(
            defined=self.filters,
            attach_to=logger_name,
            attach_to_kind='logger',
            attachees=filter_names,
            attachee_kind='filter')

        logger_filters = logger_dict.setdefault('filters', [])
        logger_filters.extend(filter_names)

        return self

    def set_logger_level(self, logger_name, level):
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
        """
        .. _config-method:

        Call ``logging.config.dictConfig()`` with the dict that has been built.
        If ``self._warn_undefined`` is false, first call ``check()`` to verify
        consistency (that everything referred to exists).

        :param disable_existing_loggers: Last chance to change this setting.

        By default, LCDs are created with

            ``self['disable_existing_loggers'] == False``

        The `logging` module defaults this setting to ``True``,

            | for reasons of backward compatibility. This may or may not be
            | what you want, since it will cause any loggers existing before
            | the [dictConfig()] call to be disabled unless they (or an ancestor)
            | are explicitly named in the configuration. ... [S]pecify False
            | for this parameter if you wish.

            (*from* `Warning in "Configuring Logging" section of logging HOWTO <https://docs.python.org/3/howto/logging.html#configuring-logging>`_)
        """
        if disable_existing_loggers is not None:
            self['disable_existing_loggers'] = bool(disable_existing_loggers)
        if not self._warn_undefined:    # 0.2.7b13
            self.check()                # 0.2.7b13
        logging.config.dictConfig(dict(self))

    def dump(self, **kwargs):                   # pragma: no cover
        """
        Prettyprint the underlying ``dict``.
        For debugging, sanity checks, etc.
        This method does NOT return ''self''.

        :param kwargs: any keyword arguments that can be passed to ``print``, e.g. ``file``.
        """
        from pprint import pformat
        print(pformat(dict(self)), **kwargs)

    # -------------------------------------------------------
    # Consistency checking
    # -------------------------------------------------------

    def check(self, verbose=True):
        """
        .. _check-method:

        Check for consistency: names used to refer to entities (formatters,
        handlers, filters) must exist (must actually have been added).

        Presently, this method doesn't check for duplicate attachments
        of handlers (or filters).

        :param verbose: If true, and if there inconsistencies, write details of
            all problems to ``stderr`` before raising ``KeyError``.

        :return: ``self`` if consistent.

        Raises ``KeyError`` if ``self`` is not consistent.
        """
        # TODO maybe: At present, this method doesn't check for
        #  |          duplicate attachments of handlers or filters

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
            if hform_name is not None and hform_name not in formatters_:
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
            # if ldict has filters (has a 'filters' key)
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
        if not self._warn_redefine:
            return
        srcfile, lineno = self._get_caller_srcfile_lineno()
        if key in subdict:
            print_err(
                "Warning (%s, line %d): redefinition of %s '%s'."
                % (srcfile, lineno, kind, key)
            )

    def _check_set_formatter(self, handler_name, formatter_name):
        if not self._warn_replace_formatter:
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
        if self._warn_reattach and dups:
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
        if self._warn_reattach and reattached:
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

    def _check_defined(self,
                       defined=None,
                       attach_to=None,
                       attach_to_kind=None,
                       attachees=None,
                       attachee_kind=None):
        """
        :param defined:
        :param attach_to:
        :param attach_to_kind:
        :param attachees:
        :param attachee_kind:
        """
        if not self._warn_undefined:
            return
        defined = defined or []

        undefined = []
        for item in attachees:
            if item not in defined:
                undefined.append(item)
        if undefined:
            srcfile, lineno = self._get_caller_srcfile_lineno()
            undefined_str = str(undefined)[1:-1]
            errmsg = (
                "Warning (%s, line %d):"
                " attaching undefined %s%s %s to %s '%s'."
                % (srcfile, lineno,
                   attachee_kind, ('s' if len(undefined) > 1 else ''),
                   undefined_str,
                   attach_to_kind, attach_to)
            )
            print_err(errmsg)

def print_err(msg, **kwargs):
    import sys
    if PY2:
        msg = unicode(msg)
    print(msg, file=sys.stderr, **kwargs)
