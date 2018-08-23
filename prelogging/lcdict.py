# coding=utf-8

from copy import deepcopy

from .lcdictbasic import LCDictBasic
from .formatter_presets import update_formatter_presets_from_file, _formatter_presets
import socket
from logging.handlers import SysLogHandler, SYSLOG_UDP_PORT
import os
from .six import PY2


__author__ = "Brian O'Neill"

__doc__ = """\
    .. include:: _global.rst
"""

# update _formatter_presets with (path to this module) + 'formatter_presets.txt'
update_formatter_presets_from_file(
    os.path.join(os.path.dirname(__file__), 'formatter_presets.txt')
)

# -----------------------------------------------------------------------
# LCDict
# -----------------------------------------------------------------------

class LCDict(LCDictBasic):
    """ \
    Except for properties and the ``__init__`` method, all public instance
    methods of this class return ``self``.

    .. _LCDict-init-params:

    .. index:: __init__ keyword parameters (LCDict)

    ``__init__`` **keyword parameters**  |br|
    ``- - - - - - - - - - - - - -``

    In addition to the parameters ``root_level``,
    ``disable_existing_loggers`` and ``warnings`` recognized by :ref:`LCDictBasic`,
    the constructor of this class accepts a few more::

            log_path                (str)
            attach_handlers_to_root (bool)
            locking                 (bool)

    ``log_path`` is a directory in which log files will be created by
    ``add_file_handler`` and ``add_rotating_file_handler``. If the filename
    passed to those methods contains a relative path, then the logfile will
    be created in that relative subdirectory of ``log_path``. If ``log_path``
    is not an absolute path, then it is relative to the current directory
    at runtime when ``config()`` is finally called.

    When ``attach_handlers_to_root`` is true [default: False], by default the
    ``add_*_handler`` methods of this class automatically attach handlers to
    the root logger after adding them to the ``handlers`` subdictionary. Each
    instance saves the value passed to its constructor, and exposes it as the
    read-only property ``attach_handlers_to_root``.

    When ``locking`` is true [default: False], by default the ``add_*_handler``
    methods of this class that can do so add :ref:`locking handlers <locking-handlers>`;
    if it's false, handlers instantiate the "usual" classes defined by `logging`.
    (See the :ref:`class inheritance diagram <prelogging-all-classes>`.)
    Each instance saves the value passed to its constructor, and exposes it as
    the read-only property ``locking``.

    All of the methods that add a handler take parameters ``attach_to_root``
    and ``locking``, each a ``bool`` or ``None``; these allow overriding of
    the values passed to the constructor. Thus, for example, callers can
    add a non-locking handler to an ``LCDict`` even if its ``locking`` property
    is true, or a locking handler even if ``locking`` is false. The default
    value of these parameters in handler-adding methods is ``None``, meaning:
    use the corresponding value passed to the constructor.
    """
    def __init__(self,                  # *,
                 root_level='WARNING',       # == logging default level
                 log_path='',
                 locking=False,
                 attach_handlers_to_root=False,
                 disable_existing_loggers=False,  # NOTE: logging default value is True
                 warnings=LCDictBasic.Warnings.DEFAULT):
        """
        :param root_level: one of ``'DEBUG'``, ``'INFO'``, ``'WARNING'``,
            ``'ERROR'``, ``'CRITICAL'``, ``'NOTSET'``
        :param log_path: is a path, absolute or relative, where logfiles will
            be created. ``add_file_handler`` prepends ``log_path`` to its
            ``filename`` parameter and uses that as the value of the
            ``'filename'`` key. Prepending uses ``os.path.join``. The directory
            specified by ``log_path`` must already exist.
        :param locking: if true, console handlers use locking stream handlers,
            and file handlers created by ``add_file_handler``,
            ``add_rotating_file_handler`` and ``add_syslog_handler``
            use locking file handlers, **unless** ``locking=False`` is passed
            to the calls that create those handlers.
        :param attach_handlers_to_root: If true, by default the handler-adding
            methods of this class will automatically attach handlers to the root
            logger.
        :param disable_existing_loggers: corresponds to the logging dict-config
            key(/value) of the same name. This default value is ``False`` so
            that separate packages can use this class to create their own
            ("private") loggers before or after their clients do their own
            logging configuration. NOTE: The `logging` default value is ``True``.
        :param warnings: as for ``LCDictBasic``. See the documentation for the inner
            class ``LCDictBasic.WARNINGS``.

        See also :ref:`__init__ keyword parameters <LCDict-init-params>`.
        """
        super(LCDict, self).__init__(
                        root_level=root_level,
                        disable_existing_loggers=disable_existing_loggers,
                        warnings=warnings)
        self.log_path = log_path
        self._locking = locking
        self._attach_handlers_to_root = attach_handlers_to_root

    @property
    def attach_handlers_to_root(self):
        """
        (r/o property) Return this logging config dict's default
        `attach_to_root` setting, used by handler-adding methods when their
        ``attach_to_root`` parameter is ``None``.

        :return: ``self._attach_to_root``, the value of
            ``attach_handlers_to_root`` passed to the constructor
        """
        return self._attach_handlers_to_root

    @property
    def locking(self):
        """
        (r/o property) Return this logging config dict's default `locking`
        setting, used by handler-adding methods when their ``locking`` parameter
        is ``None``.

        :return: ``self._locking``, the value of ``locking`` passed to
            the constructor
        """
        return self._locking

    def _attach_to_root__adjust(self, attach):
        """
        :param attach: Any; but really, ``bool`` or None.
        :return: self.attach_handlers_to_root if attach is None else bool(attach)
        """
        return self._attach_handlers_to_root if attach is None else bool(attach)

    def _locking__adjust(self, locking):
        """
        :param locking: Any; but really, ``bool`` or None.
        :return: self.locking if attach is None else bool(locking)
        """
        return self._locking if locking is None else bool(locking)

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
        attach_to_root = self._attach_to_root__adjust(attach_to_root)

        clone_dict = deepcopy(self.handlers[handler])
        # Change any 'class' key back into 'class_'
        assert 'class_' not in clone_dict
        if 'class' in clone_dict:
            clone_dict['class_'] = clone_dict.pop('class')
        # Now delegate:
        self.add_handler(clone,
                         attach_to_root=attach_to_root,
                         ** clone_dict)
        return self

    def _add_formatter_if_preset(self, formatter_name):
        if (formatter_name and
            formatter_name not in self.formatters and
            formatter_name in _formatter_presets
           ):
            self.add_formatter(formatter_name,
                               ** _formatter_presets[formatter_name].to_dict())

    def set_handler_formatter(self, handler_name, formatter_name):
        """
        Hook the LCDictBasic method so that we can add preset formatters just in time

        :return: ``self``
        """
        self._add_formatter_if_preset(formatter_name),
        return super(LCDict, self).set_handler_formatter(
                                        handler_name, formatter_name)

    def add_handler(self, handler_name,     # *,
                    formatter=None,
                    attach_to_root=None,
                    ** handler_dict):
        """
        (Virtual) Adds the ``attach_to_root`` parameter to
        ``LCDictBasic.add_handler()``.

        :param formatter: name of formatter (-spec), or name of formatter preset
        :param attach_to_root: If true, add the handler to the root logger;
            if ``None``, do what ``self.attach_handlers_to_root`` says;
            if false, don't add to root.

        :param handler_dict: Other keyword args as for LCDictBasic.add_handler,
            e.g. ``level``, ``filters``

        :return: ``self``
        """
        # Don't add all the predefined formatters to every LCDict.
        # Every LCDict handler-adding method ultimately funnels
        # through here, so we check whether ``formatter`` is
        # a name of a formatter preset; if it is, make sure it's
        # added, just in time -- add it to self.formatters
        # if it isn't there already.
        self._add_formatter_if_preset(formatter)

        super(LCDict, self).add_handler(handler_name,
                                        formatter=formatter,
                                        ** handler_dict)
        if self._attach_to_root__adjust(attach_to_root):
            super(LCDict, self).attach_root_handlers(handler_name)
        return self

    def add_stream_handler(self, handler_name,    # *,
                           stream,
                           locking=None,
                           **kwargs):
        """
        :param handler_name: just that
        :param stream: stream or name of stream, e.g. ``sys.stderr``
            or ``'ext://sys.stderr'``
        :param locking: If true, this handler will be a
            :ref:`LockingStreamHandler <LockingStreamHandler>`;
            if ``None``, do what ``self.locking`` says;
            if false, the handler will be a ``logging.StreamHandler``.
        :param kwargs: Other keyword args as for LCDict.add_handler,
            LCDictBasic.add_handler, e.g. ``level``, ``formatter``,
            ``attach_to_root``, ``filters``
        :return: ``self``
        """
        # self can be created with (self.)locking=False,
        # but a handler can be locking.
        locking = self._locking__adjust(locking)
        if locking:
            kwargs['()'] = 'ext://prelogging.LockingStreamHandler'
            kwargs['create_lock'] = True
        else:
            kwargs['class_'] = 'logging.StreamHandler'

        self.add_handler(handler_name,
                         stream=stream,
                         ** kwargs)
        return self

    def add_stdout_handler(self, handler_name,  # *,
                           **kwargs):
        """Add a console (stream) handler that writes to ``sys.stdout``.

        :param kwargs: Keyword args for
            add_stream_handler, LCDict.add_handler, LCDictBasic.add_handler,
            e.g. ``locking``, ``level``, ``formatter``, ``attach_to_root``, ``filters``
        :return: ``self``
        """
        self.add_stream_handler(handler_name,
                                stream='ext://sys.stdout',
                                **kwargs)
        return self

    def add_stderr_handler(self, handler_name,  # *,
                           **kwargs):
        """Add a console (stream) handler that writes to ``sys.stderr``.

        :param kwargs: Keyword args for
            add_stream_handler, LCDict.add_handler, LCDictBasic.add_handler,
            e.g. ``locking``, ``level``, ``formatter``, ``attach_to_root``, ``filters``
        :return: ``self``
        """
        self.add_stream_handler(handler_name,
                                stream='ext://sys.stderr',
                                **kwargs)
        return self

    def add_file_handler(self, handler_name,    # *,
                         filename,
                         formatter=None,
                         mode='a',
                         encoding=None,
                         delay=False,       # `logging` default
                         locking=None,
                         **kwargs):
        """
        (Virtual) Adds keyword parameters ``locking`` and ``attach_to_root``
        to the parameters of ``LCDictBasic.add_file_handler()``.

        :param kwargs: Keyword args for
            LCDict.add_handler, LCDictBasic.add_handler,
            e.g. ``attach_to_root``, ``level``, ``filters``
        :return: ``self``
        """
        # So: self can be created with (self.)locking=False,
        # but a handler can be locking.
        locking = self._locking__adjust(locking)

        if not formatter:
            formatter = ('process_time_logger_level_msg'
                         if locking else
                         'time_logger_level_msg')
        self.add_handler(handler_name,
                         class_='logging.FileHandler',
                         filename=os.path.join(self.log_path, filename),
                         mode=mode,
                         encoding=encoding,
                         delay=delay,
                         formatter=formatter,
                         **kwargs)
        if locking:
            del self.handlers[handler_name]['class']
            self.handlers[handler_name]['()'] = 'ext://prelogging.LockingFileHandler'
            self.handlers[handler_name]['create_lock'] = True
        return self

    def add_rotating_file_handler(self, handler_name,   # *,
                         filename,
                         max_bytes=0,       # logging default
                         backup_count=0,    # logging default
                         formatter=None,
                         mode='a',
                         encoding=None,
                         delay=False,       # `logging` default
                         locking=None,
                         **kwargs):
        """
        :param handler_name: just that
        :param filename: just that
        :param max_bytes: logfile size threshold. Given logfile name ``lf.log``,
            if a write would cause ``lf.log`` to exceed this size,
            the following occurs, where `K` = backup_count:
            if ``lf.log.``\ `K` exists it is deleted;
            all files ``lf.log.1``, ``lf.log.2``, ... ``lf.log.``\ `K-1`
            are renamed to ``lf.log.2``, ``lf.log.3``, ... ``lf.log.``\ `K`;
            ``lf.log`` is closed, and renamed to ``lf.log.1``;
            a new ``lf.log`` is created and written to.
            The `logging` oackage calls this parameter ``maxBytes``, where it
            also defaults to 0.
        :param backup_count: max number of backup files to create and
            maintain. The `logging` package calls this parameter ``backupCount``,
            where it also defaults to 0.
        :param formatter: the name of the formatter that this handler will use
        :param mode: the mode in which the logfile is opened
        :param encoding: if encoding is not None, the file is opened with that
            encoding
        :param delay: if True, the log file won't be created until it's
            actually written to
        :param locking: Mandatory if multiprocessing -- things won't even work,
            logfile can't be found: FileNotFoundError: [Errno 2]...
        :param kwargs: Keyword args for
            LCDict.add_handler, LCDictBasic.add_handler,
            e.g. ``level``, ``attach_to_root``, ``filters``
        :return: ``self``
        """
        locking = self._locking__adjust(locking)

        if not formatter:
            formatter = ('process_time_logger_level_msg'
                         if locking else
                         'time_logger_level_msg')
        self.add_handler(handler_name,
                         class_='logging.handlers.RotatingFileHandler',
                         filename=os.path.join(self.log_path, filename),
                         mode=mode,
                         encoding=encoding,
                         delay=delay,
                         formatter=formatter,
                         maxBytes=max_bytes,
                         backupCount=backup_count,
                         **kwargs)
        if locking:
            del self.handlers[handler_name]['class']
            self.handlers[handler_name]['()'] = \
                'ext://prelogging.LockingRotatingFileHandler'
            self.handlers[handler_name]['create_lock'] = True
        return self

    def add_null_handler(self, handler_name,  # *
                         **kwargs):
        """Add a ``logging.NullHandler``.

        :param handler_name: name of the handler
        :param level: the handler's loglevel
        :param attach_to_root: If true, add the handler to the root
            logger; if ``None``, do what ``self.attach_handlers_to_root`` says;
            if false, don't add to root.
        :param kwargs: Keyword args for
            LCDict.add_handler, LCDictBasic.add_handler,
            e.g. ``attach_to_root``, ``level``, ``filters``
        :return: ``self``
        """
        return self.add_handler(
            handler_name,
            class_='logging.NullHandler',
            **kwargs)

    def add_syslog_handler(self, handler_name,   # *,
                         address=('localhost', SYSLOG_UDP_PORT),
                         facility=SysLogHandler.LOG_USER,
                         socktype=socket.SOCK_DGRAM,
                         locking=None,
                         **kwargs):
        """
        :param handler_name: just that

        See the
        `SysLogHandler documentation <https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SysLogHandler>`_
        for details about the next three parameters:

        :param address:  as for logging.handlers.SysLogHandler
        :param facility: `ditto`
        :param socktype: `ditto`

        On OS X, use ``address='/var/run/syslog'`` to write to the system log
        (``system.log``); on \*nix, use ``address='/dev/log'``.

        :param locking: if false, use ``logging.handlers.SysLogHandler``;
            if ``None``, do what ``self.locking`` says;
            if true, use the multiprocessing-safe version of that handler.
        :param kwargs: Keyword args for
            LCDict.add_handler, LCDictBasic.add_handler,
            e.g. ``formatter``, ``attach_to_root``, ``level``, ``filters``
        :return: ``self``
        """
        locking = self._locking__adjust(locking)

        self.add_handler(handler_name,
                         class_='logging.handlers.SysLogHandler',
                         address=address,
                         facility=facility,
                         socktype=socktype,
                         **kwargs)
        if locking:
            del self.handlers[handler_name]['class']
            self.handlers[handler_name]['()'] = \
                'ext://prelogging.LockingSysLogHandler'
            self.handlers[handler_name]['create_lock'] = True
        return self

    def add_email_handler(self,
                          handler_name,  # *
                          # filters=None,
                          # SMTPHandler-specific:
                          mailhost=None,  # e.g. 'smtp.gmail.com'
                          fromaddr=None,     # str
                          toaddrs=None,      # str or list of strs
                          subject=None,      # str
                          secure=(),         #
                          # credentials=(SMTP_USERNAME, SMTP_PASSWORD),
                          username=None,     # str
                          password=None,     # str
                          timeout=None,      # sec
                          # Other
                          **kwargs):
        """Add specifications for an
        `SMTPHandler <https://docs.python.org/3/library/logging.handlers.html#smtphandler>`_
        to the logging config dict.

        :param handler_name: name of this handler
        :param level: loglevel of this handler
        :param formatter: ``str``, name of formatter

        ``SMTPHandler``-specific parameters, quoting extensively from the
        `logging` docs:

        :param mailhost: name of SMTP server e.g. 'smtp.gmail.com'
        :param fromaddr: email address of sender (``str``)
        :param toaddrs:  email recipients (``str`` or ``list`` of ``str``\ s)
        :param subject:  subject of the email (``str``)
        :param secure:  To specify the use of a secure
            protocol (TLS), pass a tuple for this argument. This will only be
            used when authentication credentials are supplied. The tuple should
            be either an empty tuple, or a single-value tuple with the name of
            a keyfile, or a 2-value tuple with the names of the keyfile and
            certificate file. (This tuple is passed to the
            smtplib.SMTP.starttls() method.)

        :param username: SMTP username of sender
        :param password: SMTP password of sender with username provided.
            As a tuple, ``username`` and ``password`` form the `credentials`
            parameter expected by the SMTPHandler constructor
        :param timeout: Timeout (seconds) for communication with the SMTP server
            or 0.0 or 0 or None or < 0 to indicate "no timeout"
        :param kwargs: Keyword args for
            LCDict.add_handler, LCDictBasic.add_handler,
            e.g. ``formatter``, ``attach_to_root``, ``level``, ``filters``
        :return: ``self``
        """
        if (timeout is not None and timeout != 0.0
            and int(timeout) != 0 and timeout > 0):
            kwargs['timeout'] = timeout

        return self.add_handler(
            handler_name,
            class_='logging.handlers.SMTPHandler',
            # SMTPHandler-specific kwargs:
            mailhost=mailhost,
            fromaddr=fromaddr,
            toaddrs=toaddrs,
            subject=subject,
            secure=secure,
            credentials=(username, password),
            # timeout=timeout,
            **kwargs)

    def add_queue_handler(self,
                          handler_name,
                          # QueueHandler-specific:
                          queue=None,
                          **kwargs):
        """(*Python 3 only*)

        :param handler_name: the name of this handler
        :param level: the loglevel of this handler (best left at its default)
        :param queue: an actual queue object (``multiproccessing.Queue``).
            Thus, **don't** use ``clone_handler`` on a queue handler!

        :param kwargs: Keyword args for
            LCDict.add_handler, LCDictBasic.add_handler,
            e.g. ``formatter``, ``attach_to_root``, ``level``, ``filters``
        :return: ``self``
        """
        if PY2:
            raise NotImplementedError("logging.handlers.QueueHandler"
                                      " doesn't exist in Python 2")
        return self.add_handler(
            handler_name,
            class_='logging.handlers.QueueHandler',
            queue=queue,
            **kwargs)

    # add_*_filter methods

    def add_class_filter(self, filter_name, filter_class, **filter_init_kwargs):
        """
        A convenience method for adding a class filter, a class that implements
        a ``filter`` method of signature ``(logging.LogRecord) -> bool``
        (omitting ``self``).

        This method spares you from writing:

            ``self.add_filter(filter_name, ** {'()': filter_class})``

        (or even more elaborate code, if ``filter_class`` takes keyword
        arguments, available in ``filter_init_kwargs``).

        :param filter_name: name of the filter (for attaching it to handlers
            and loggers)
        :param filter_class: a class implementing a ``filter`` method of
            signature ``(logging.LogRecord) -> bool``.
        :param filter_init_kwargs: any other parameters to be passed to
            ``add_filter``. These will be passed to the ``filter_class``
            constructor. See the documentation for
            ``LCDictBasic.add_filter``.
        :return: ``self``
        """
        filter_init_kwargs['()'] = filter_class
        return self.add_filter(filter_name, **filter_init_kwargs)

    def add_callable_filter(self, filter_name, filter_fn, **filter_init_kwargs):
        """A convenience method for adding a callable filter of signature
        ``(logging.LogRecord, **kwargs) -> bool``. This method spares you from
        having to write code like the following:

            ``self.add_filter(filter_name, ** {'()': lambda: filter_fn})``

        (or worse, if ``filter_fn`` takes keyword arguments), and, under Python
        2, having to also write

            ``filter_fn.filter = filter_fn``.

        :param filter_name: name of the filter (for attaching it to handlers
            and loggers)
        :param filter_fn: a callable, of signature
            ``(logging.LogRecord, **kwargs) -> bool``.
            A record is logged iff this callable returns true.
        :param filter_init_kwargs: Keyword arguments that will be passed to
            the filter_fn **each time it is called**. To pass dynamic data,
            you can't just wrap it in a list or dict; use an object or callable
            instead. See the documentation for an example of how to do that.

            Note that this method is like "partial": it provides a kind
            of Currying.
        :return: ``self``
        """
        class FilterMaker():
            def __init__(self, callable_filter=None, ** callable_filter_kwargs):
                self.callable_filter = callable_filter
                self.filter_callable_kwargs = callable_filter_kwargs

            def filter(self, record):
                return self.callable_filter(record,
                                            ** self.filter_callable_kwargs)

        filter_init_kwargs['callable_filter'] = filter_fn
        return self.add_class_filter(filter_name, FilterMaker, **filter_init_kwargs)

        # Former implementation, pre-filter-kwargs, pre FilterMaker class:
        # Paper over a difference between how Python 2 and Python 3
        # handle callable filters:
        #
        # if PY2:      # curious lil hack
        #     if not hasattr(filter_fn, 'filter'):
        #         setattr(filter_fn, 'filter', filter_fn)
        # filter_dict['()'] = lambda: filter_fn
        # return self.add_filter(filter_name, ** filter_dict)
