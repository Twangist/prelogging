# coding=utf-8

import os
from copy import deepcopy

from .logging_config_dict import LoggingConfigDict
from ._version import IS_PY2

__doc__ = """\
"""

__author__ = "Brian O'Neill"

class LoggingConfigDictEx(LoggingConfigDict):
    """ \
    A ``LoggingConfigDict`` subclass with a few batteries included — formatters,
    various handler-creators, multiprocessing-aware handlers that output to the
    console, to files and to rotating files.

    .. include:: _global.rst

    Except for ``__init__`` and ``add_*_filter`` methods, every method of this
    class adds a handler of some kind. All methods except ``__init__`` return
    ``self``.


    .. _LoggingConfigDictEx-init-params:

    .. index:: __init__ keyword parameters (LoggingConfigDictEx)

    ``__init__`` **keyword parameters**  |br|
    ``- - - - - - - - - - - - - - - - - - - - - - - - -``

    In addition to the parameters ``root_level`` and
    ``disable_existing_loggers`` recognized by :ref:`LoggingConfigDict`,
    the constructor of this class accepts a few more::

            attach_handlers_to_root (bool)
            locking                 (bool)
            log_path                (str)

    When ``attach_handlers_to_root`` is true, by default the other methods
    of this class automatically add handlers to the root logger as well as
    to the ``handlers`` subdictionary. By default, ``attach_handlers_to_root``
    is ``False``.

    When ``locking`` is true, by default the other methods of this class
    add :ref:`locking handlers <locking-handlers>`; if it's false, handlers
    instantiate the "usual" classes defined by `logging`. (See the
    :ref:`class inheritance diagram <lcd-all-classes>`.)
    By default, ``locking`` is ``False``.

    All of the methods that add a handler take parameters ``attach_to_root``
    and ``locking``, each a ``bool`` or ``None``; these allow overriding of
    the values established by ``__init__``. Thus, for example, callers can
    add a non-locking handler even if ``self.locking`` is true, or a locking
    handler even if ``self.locking`` is false. The default value of these
    parameters of handler-adding methods is ``None``, meaning: use the value
    of the attribute on ``self``.

    ``log_path`` is a directory in which log files will be created by
    ``add_file_handler`` and ``add_rotating_file_handler``. If the filename
    passed to those methods contains a relative path, then the logfile will
    be created in that relative subdirectory of ``log_path``. If ``log_path``
    is not an absolute path, then it is relative to the current directory
    at runtime when ``config()`` is finally called.

    .. _builtin-formatters:

    .. index:: Builtin Formatters (LoggingConfigDictEx)

    **Formatters provided** |br|
    ``- - - - - - - - - - - - - - - - - - - - - - - - -``

    Their names make it fairly obvious what their format strings are:

    +---------------------------------------+------------------------------------------------------------------------------------+
    || Formatter name                       || Format string                                                                     |
    +=======================================+====================================================================================+
    || ``'minimal'``                        || ``'%(message)s'``                                                                 |
    +---------------------------------------+------------------------------------------------------------------------------------+
    || ``'level_msg'``                      || ``'%(levelname)-8s: %(message)s'``                                                |
    +---------------------------------------+------------------------------------------------------------------------------------+
    || ``'process_msg'``                    || ``'%(processName)-10s: %(message)s'``                                             |
    +---------------------------------------+------------------------------------------------------------------------------------+
    || ``'logger_process_msg'``             || ``'%(name)-20s: %(processName)-10s: %(message)s'``                                |
    +---------------------------------------+------------------------------------------------------------------------------------+
    || ``'logger_level_msg'``               || ``'%(name)-20s: %(levelname)-8s: %(message)s'``                                   |
    +---------------------------------------+------------------------------------------------------------------------------------+
    || ``'logger_msg'``                     || ``'%(name)-20s: %(message)s'``                                                    |
    +---------------------------------------+------------------------------------------------------------------------------------+
    || ``'process_level_msg'``              || ``'%(processName)-10s: %(levelname)-8s: %(message)s'``                            |
    +---------------------------------------+------------------------------------------------------------------------------------+
    || ``'process_time_level_msg'``         || ``'%(processName)-10s: %(asctime)s: %(levelname)-8s: %(message)s'``               |
    +---------------------------------------+------------------------------------------------------------------------------------+
    || ``'process_logger_level_msg'``       || ``'%(processName)-10s: %(name)-20s: %(levelname)-8s: %(message)s'``               |
    +---------------------------------------+------------------------------------------------------------------------------------+
    || ``'process_time_logger_level_msg'``  || ``'%(processName)-10s: %(asctime)s: %(name)-20s: %(levelname)-8s: %(message)s'``  |
    +---------------------------------------+------------------------------------------------------------------------------------+
    || ``'time_logger_level_msg'``          || ``'%(asctime)s: %(name)-20s: %(levelname)-8s: %(message)s'``                      |
    +---------------------------------------+------------------------------------------------------------------------------------+

    """

    format_strs = {
        'minimal':
            '%(message)s',
        'level_msg':
            '%(levelname)-8s: %(message)s',
        'process_msg':
            '%(processName)-10s: %(message)s',
        'logger_process_msg':
            '%(name)-20s: %(processName)-10s: %(message)s',
        'logger_level_msg':
            '%(name)-20s: %(levelname)-8s: %(message)s',
        'logger_msg':
            '%(name)-20s: %(message)s',
        'process_level_msg':
            '%(processName)-10s: %(levelname)-8s: %(message)s',
        'process_time_level_msg':
            '%(processName)-10s: %(asctime)s: %(levelname)-8s: %(message)s',
        'process_logger_level_msg':
            '%(processName)-10s: %(name)-20s: %(levelname)-8s: %(message)s',
        'process_time_logger_level_msg':
            '%(processName)-10s: %(asctime)s:'
            ' %(name)-20s: %(levelname)-8s: %(message)s',
        'time_logger_level_msg':
            '%(asctime)s: %(name)-20s: %(levelname)-8s: %(message)s',
    }

    def __init__(self,                  # *,
                 root_level='WARNING',       # == logging default level
                 log_path='',
                 locking=False,
                 attach_handlers_to_root=False,
                 disable_existing_loggers=False):  # logging default value is True
        """
        :param root_level: one of ``'DEBUG'``, ``'INFO'``, ``'WARNING'``,
            ``'ERROR'``, ``'CRITICAL'``, ``'NOTSET'``
        :param log_path: is a path, absolute or relative, where logfiles will
            be created. ``add_file_handler`` prepends ``log_path`` to its
            ``filename`` parameter and uses that as the value of the
            ``'filename'`` key. Prepending uses ``os.path.join``. The directory
            specified by ``log_path`` must already exist.
        :param locking: if True, console handlers use locking stream handlers,
            and file handlers created by ``add_file_handler`` and
            ``add_rotating_file_handler`` use locking file handlers, **unless**
            ``locking=False`` is passed to the calls that create those handlers.
        :param attach_handlers_to_root: If true, by default the other methods
            of this class will automatically add handlers to the root logger,
            as well as to the ``handlers`` subdictionary.
        :param disable_existing_loggers: corresponds to the logging dict-config
            key(/value) of the same name. This default value is ``False`` so
            that separate packages can use this class to create their own
            ("private") loggers before or after their clients do their own
            logging configuration. The `logging` default value is ``True``.

        See also :ref:`__init__ keyword parameters <LoggingConfigDictEx-init-params>`
        above, in the class's docstring.
        """
        super(LoggingConfigDictEx, self).__init__(
                        root_level=root_level,
                        disable_existing_loggers=disable_existing_loggers)
        self.log_path = log_path
        self.locking = locking
        self.attach_handlers_to_root = attach_handlers_to_root

        # Include some batteries (Formatters) --
        # The default is class_='logging.Formatter'
        for formatter_name in self.format_strs:
            self.add_formatter(formatter_name,
                               format=self.format_strs[formatter_name])

    def _attach_to_root(self, attach):
        """
        :param attach: Any; but really, ``bool`` or None.
        :return: self.attach_handlers_to_root if attach is None else bool(attach)
        """
        return self.attach_handlers_to_root if attach is None else bool(attach)

    def clone_handler(self,     # *,
                      clone,
                      handler,
                      attach_to_root=None):
        """Add a handler named by ``clone`` whose handler dictionary is a deep
        copy of the dictionary of the handler named by ``handler``.

        **Note**: if the handler named  by ``clone`` already exists,
        its settings will be replaced by those of ``handler``.

        :param clone: name of a (usually new) handler — the target.
        :param handler: name of existing, source handler. Raise ``KeyError``
            if no such handler has been added.
        :param attach_to_root: If true, add the ``clone`` handler to the root
            logger; if ``None``, do what ``self.attach_handlers_to_root`` says;
            if false, don't add clone to root.
        :return: ``self``
        """
        attach_to_root = self._attach_to_root(attach_to_root)

        clone_dict = deepcopy(self.handlers[handler])
        # Change any 'class' key back into 'class_'
        assert 'class_' not in clone_dict
        if 'class' in clone_dict:
            clone_dict['class_'] = clone_dict.pop('class')
        # Now defer:
        self.add_handler(clone,
                         attach_to_root=attach_to_root,
                         ** clone_dict)
        return self

    def add_handler(self, handler_name,     # *,
                    attach_to_root=None,
                    ** handler_dict):
        """Virtual; adds the ``attach_to_root`` parameter to
        ``LoggingConfigDict.add_handler()``.

        :return: ``self``
        """
        super(LoggingConfigDictEx, self).add_handler(handler_name, ** handler_dict)
        if self._attach_to_root(attach_to_root):
            super(LoggingConfigDictEx, self).attach_root_handlers(handler_name)
        return self

    def _add_console_handler(self, handler_name,    # *,
                             stream,
                             formatter=None,
                             level='WARNING',   # logging module default: 'NOTSET'
                             locking=None,
                             attach_to_root=None,
                             **kwargs):
        """
        :param handler_name:
        :param stream:
        :param formatter:
        :param level:
        :param locking: If true, this handler will be a
            :ref:`LockingStreamHandler`; if false, the handler will be a
            ``logging.StreamHandler``.
        :param attach_to_root: If true, add the ``clone`` handler to the root
            logger; if ``None``, do what ``self.attach_handlers_to_root`` says;
            if false, don't add clone to root.
        :param kwargs:
        :return: ``self``
        """
        # So: self can be created with (self.)locking=False,
        # but a handler can be locking.
        locking = self.locking if locking is None else bool(locking)
        attach_to_root = self._attach_to_root(attach_to_root)

        if formatter is None:
            formatter = ('process_logger_level_msg'
                         if locking else
                         'logger_level_msg')
        con_dict = dict(level=level, formatter=formatter, ** kwargs)
        if locking:
            con_dict['()'] = 'ext://lcd.LockingStreamHandler'
            con_dict['create_lock'] = True
        else:
            con_dict['class_'] = 'logging.StreamHandler'

        self.add_handler(handler_name,
                         stream=stream,
                         attach_to_root=attach_to_root,
                         ** con_dict)
        return self

    def add_stdout_console_handler(self, handler_name,  # *,
                             formatter=None,
                             level='WARNING',
                             locking=None,
                             attach_to_root=None,
                             **kwargs):
        """Add a console (stream) handler that writes to ``sys.stdout``.

        :return: ``self``
        """
        self._add_console_handler(handler_name,
                                  stream='ext://sys.stdout',
                                  formatter=formatter,
                                  level=level,
                                  locking=locking,
                                  attach_to_root=attach_to_root,
                                  **kwargs)
        return self

    def add_stderr_console_handler(self, handler_name,  # *,
                             formatter=None,
                             level='WARNING',
                             locking=None,
                             attach_to_root=None,
                             **kwargs):
        """Add a console (stream) handler that writes to ``sys.stderr``.

        :return: ``self``
        """
        self._add_console_handler(handler_name,
                                  stream='ext://sys.stderr',
                                  formatter=formatter,
                                  level=level,
                                  locking=locking,
                                  attach_to_root=attach_to_root,
                                  **kwargs)
        return self

    def add_file_handler(self, handler_name,    # *,
                         filename,
                         formatter=None,
                         mode='w',
                         level='NOTSET',    # log everything: logging module default
                         delay=False,       # logging module default
                         locking=None,
                         attach_to_root=None,
                         **kwargs):
        """Virtual; adds keyword parameters ``locking`` and ``attach_to_root``
        to the parameters of ``LoggingConfigDict.add_file_handler()``.

        :return: ``self``
        """
        # So: self can be created with (self.)locking=False,
        # but a handler can be locking.
        locking = self.locking if locking is None else bool(locking)
        attach_to_root = self._attach_to_root(attach_to_root)

        if not formatter:
            formatter = ('process_time_logger_level_msg'
                         if locking else
                         'time_logger_level_msg')
        self.add_handler(handler_name,
                         class_='logging.FileHandler',
                         filename=os.path.join(self.log_path, filename),
                         mode=mode,
                         level=level,
                         formatter=formatter,
                         delay=delay,
                         attach_to_root=attach_to_root,
                         **kwargs)
        if locking:
            del self.handlers[handler_name]['class']
            self.handlers[handler_name]['()'] = 'ext://lcd.LockingFileHandler'
            self.handlers[handler_name]['create_lock'] = True
        return self

    def add_rotating_file_handler(self, handler_name,   # *,
                         filename,
                         max_bytes=0,       # logging.handlers default
                         backup_count=0,    # logging.handlers default
                         formatter=None,
                         mode='a',
                         level='NOTSET',
                         delay=False,       # logging module default
                         locking=None,
                         attach_to_root=None,
                         **kwargs):
        """
        :param handler_name: just that
        :param filename: just that
        :param max_bytes: logfile size threshold. Given logfile name `lf.log`,
            if a write would cause `lf.log` to exceed this size,
            the following occurs, where K = backup_count:
            if `lf.log.K` exists it is deleted;
            all files `lf.log.1`, `lf.log.2`, ... `lf.log.K-1`
            are renamed to `lf.log.2`, `lf.log.3`, ... `lf.log.K`;
            `lf.log` is closed, and renamed to `lf.log.1`;
            a new `lf.log` is created and written to.
            The logging module calls this parameter `maxBytes`;
            it also defaults to 0.
        :param backup_count: (max) n)umber of backup files to create and
            maintain. The logging module calls this parameter `backupCount`;
            it also defaults to 0.
        :param formatter: the name of the formatter that this handler will use
        :param mode: NOTE -- mode is `append`, logging module default
        :param level: the loglevel of this handler
        :param delay: if True, the log file won't be created until it's
            actually written to
        :param locking: Mandatory if multiprocessing -- things won't even work,
            logfile can't be found: FileNotFoundError: [Errno 2]...
        :param attach_to_root: If true, add the ``clone`` handler to the root
            logger; if ``None``, do what ``self.attach_handlers_to_root`` says;
            if false, don't add clone to root.
        :param kwargs: additional key/value pairs
        :return: ``self``
        """
        # So: self can be created with (self.)locking=False,
        # but a handler can be locking.
        locking = self.locking if locking is None else bool(locking)
        attach_to_root = self._attach_to_root(attach_to_root)

        if not formatter:
            formatter = ('process_time_logger_level_msg'
                         if locking else
                         'time_logger_level_msg')
        self.add_handler(handler_name,
                         class_='logging.handlers.RotatingFileHandler',
                         filename=os.path.join(self.log_path, filename),
                         mode=mode,
                         level=level,
                         formatter=formatter,
                         delay=delay,
                         attach_to_root=attach_to_root,
                         maxBytes=max_bytes,
                         backupCount=backup_count,
                         **kwargs)
        if locking:
            del self.handlers[handler_name]['class']
            self.handlers[handler_name]['()'] = 'ext://lcd.LockingRotatingFileHandler'
            self.handlers[handler_name]['create_lock'] = True
        return self

    # . 0.2.7 -- Two convenience methods, so callers don't have to copy/paste
    # .          weird syntax, & so that we don't have to explain it in docs.

    def add_class_filter(self, filter_name, filter_class, ** filter_dict):
        """A convenience method for adding a class filter, an instance of
        a subclass of ``logging.Filter``. This method spares you from having
        to write code like the following:

            ``self.add_filter(filter_name, ** {'()': filter_class})``

        :param filter_name: name of the filter (for attaching it to handlers
            and loggers)
        :param filter_class: a class, subclass of ``logging.Filter``.
        :param filter_dict: any other parameters to be passed to ``add_filter``.
        :return: ``self``
        """
        filter_dict['()'] = filter_class
        return self.add_filter(filter_name, ** filter_dict)

    def add_function_filter(self, filter_name, filter_fn, ** filter_dict):
        """A convenience method for adding a callable filter, of signature
        ``logging.LogRecord -> bool``. This method spares you from having
        to write code like the following:

            ``self.add_filter(filter_name, ** {'()': lambda: filter_fn})``

        It also papers over a difference between how Python 2 and Python 3
        handle callable filters.

        :param filter_name: name of the filter (for attaching it to handlers
            and loggers)
        :param filter_fn: a callable, of signature ``logging.LogRecord -> bool``
        :param filter_dict: any other parameters to be passed to ``add_filter``.
        :return: ``self``
        """
        if IS_PY2:      # curious lil hack
            if not hasattr(filter_fn, 'filter'):
                setattr(filter_fn, 'filter', filter_fn)
        filter_dict['()'] = lambda: filter_fn
        return self.add_filter(filter_name, ** filter_dict)

# TODO  Support for  ColorizedStreamHandler?
