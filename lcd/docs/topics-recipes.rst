Topics and Recipes
====================

.. include:: _global.rst

* ``LCD``
    .. hlist::
        :columns: 3

        * :ref:`Basic usage and principles<tr-basic-usage-LCD>`
        * :ref:`overview-example-using-only-LCD`

* ``LCDEx``
    * :ref:`tr-basic-LCDEx`

* Formatters
    .. hlist::
        :columns: 3

        * :ref:`tr-LCDEx-using-builtin-formatters`
        * :ref:`tr-LCDEx-defining-new-formatters`

* Configuring the root logger
    .. hlist::
        :columns: 3

        * :ref:`tr-easy-config-root-add-console`
        * :ref:`tr-easy-config-root-add-file`
        * :ref:`tr-config-root-use-children`

* Configuring and using root and non-root loggers together
    .. hlist::
        :columns: 3

        * :ref:`tr-config-non-root-propagate`
        * :ref:`tr-config-discrete-non-root`


* :ref:`using-lcd-with-django`

* :ref:`error- checking`

|br|

* Rotating file handlers
    * :ref:`tr-rot-fh`

* :ref:`Multiprocessing — two approaches<tr-mp>`
    .. hlist::
        :columns: 3

        * :ref:`mp-locking-handlers`
        * :ref:`mp-queue-and-logging-thread`

* Filters
    .. hlist::
        :columns: 3

        * :ref:`tr-filters-logger`
        * :ref:`tr-filters-handler`
        * :ref:`passing-initialization-data-to-a-filter`
        * :ref:`passing-dynamic-data-to-a-filter`


* Configuration distributed across multiple modules or packages
    * :ref:`config-abc`

* Using other `logging` handler classes
    .. hlist::
        :columns: 3

        * :ref:`null-handler`
        * :ref:`smtp-handler`


--------------------------------------------------

.. _tr-basic-usage-LCD:

Basic usage of ``LCD``
-------------------------------------------------------

.. todo::
    intro blather, basic usage of ``LCD``

Cite :ref:`LCD`: introduction for basic usage,
and reference // OR (todo): move that material to here.
???

The :ref:`overview` contains :ref:`an example <example-overview-config>` showing
how easy it is using ``LCDEx`` to
configure the root logger with both a console handler and a file handler.
The solution shown there takes advantage of a few conveniences provided by
``LCDEx``. It's instructive to see how the same result can be
achieved using only ``LCD``.

.. _overview-example-using-only-LCD:

The Overview example, using only ``LCD``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

If we were to use just the base class ``LCD``, the Overview
example becomes just a little less concise. Now, we have to add two formatters,
and we must explicitly attach the two handlers to the root logger (two passages
which we've commented as ``# NEW``):

.. code::

    from lcd import LCD

    lcd = LCD(root_level='DEBUG')

    # NEW
    lcd.add_formatter('minimal',
                      format='%(message)s'
    ).add_formatter('logger_level_msg',
                    format='%(name)-20s: %(levelname)-8s: %(message)s'
    )

    lcd.add_handler('console',
                    formatter='minimal',
                    level='INFO',
                    class_='logging.StreamHandler',
    ).add_file_handler('file_handler',
                       formatter='logger_level_msg',
                       level='DEBUG',
                       filename='blather.log',
    )

    # NEW
    lcd.attach_root_handlers('console', 'file_handler')

    lcd.config()


--------------------------------------------------

.. _tr-basic-LCDEx:

What ``LCDEx`` contributes
---------------------------------------------------------

<<<<< TODO >>>>> 

.. todo::
    intro blather re  ``LCDEx``: why this superclass,
    what does it do, offer?

--------------------------------------------------

.. _tr-LCDEx-using-formatters:

Using formatters
-------------------------------------------------------

<<<<< TODO >>>>> 

.. _tr-LCDEx-using-builtin-formatters:

Using builtin formatters
++++++++++++++++++++++++++
<<<<< TODO >>>>>

.. _tr-LCDEx-defining-new-formatters:

Defining new formatters
++++++++++++++++++++++++++

The `logging` module supports a large number of keywords
that can appear in formatters — for a complete list, see the documentation for
`LogRecord attributes <https://docs.python.org/3/library/logging.html?highlight=logging#logrecord-attributes>`_.
Each logged message can even include the name of the function, and/or the line number,
where its originating logging call was issued.

    .. note::
        `logger` parameter names are all over the place. We allow
        fmt, format -- synonyms
        datefmt, dateformat -- synonyms


Selecting the style of the format string
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo::
    INCORPORATE :

    The ``style`` parameter to ``Formatter.__init__`` lets you use any of
    Python's three format styles in the format string used by a ``Formatter``.
    Although the documentation for logging configuration doesn't mention it,
    ``style`` also works in logging config dicts.

    .. note:: SUB-TODO:
            It IS implemented ( in Py3.5, anyway:
            Check/ TEST that/ IF it works in Py2.7 ALSO. )

            TODO Do a test too (Py2.7 support?)

    The value of ``style`` can be one of the following:

    |    ``'%'``     old-style, ``%``-based formatting
    |    ``'{'``     new-style formatting, using ``str.format``
    |    ``'$'``     template-based formatting

        A little example:

            >>> import lcd
            >>> import logging
            >>> lcdx = lcd.LCDEx(attach_handlers_to_root=True)
            # >>> lcdx.add_formatter('testform', format='{levelname} {name} {message}', style='{')
            >>> lcdx.add_formatter('testform', format='%(levelname)s %(name)s %(message)s', style='%')
            >>> lcdx.add_stderr_handler('con', formatter='testform')
            >>> lcdx.config()
            >>> root = logging.getLogger()
            >>> root.warning('Hi there')
            WARNING Hi there

        <<<<<<< See IF it works on Py2.7 >>>>>>>

        style: Try all 3 styles
            '%' old-style
            '{' new-style       # checked, works
            '$' (template-based... easy enough to figure out, maybe don't go on about it)

    Using 'datefmt' (and 'dateformat') parameter
        Give a reference (link) to what this string can be (Py logging docs)

    Using 'fmt'

    Using both ``format`` and ``fmt`` (``format`` wins)
    Using both ``datefmt`` and ``dateformat`` (``datefmt`` wins)


--------------------------------------------------


.. _tr-easy-config-root:

Configuring the root logger
------------------------------------------

We already saw :ref:`one example <example-overview-config>` of how easy it is to
configure the root logger with both a console handler and a file handler.

.. _tr-easy-config-root-add-console:

Adding a console handler
++++++++++++++++++++++++++
<<<<< TODO >>>>> 

.. _tr-easy-config-root-add-file:

Adding a file handler
++++++++++++++++++++++++++
<<<<< TODO >>>>> 

.. _tr-config-root-use-children:

Using non-root (named, child) loggers without configuring them
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A typical, useful approach is to attach handlers only to the root logger,
and then have each module log messages using ``logging.getLogger(__name__)``.
These "child" loggers require no configuration; they use the handlers
of the root because, by default, loggers are created with ``propagate=True``.

If the formatters of the handlers include the logger name — as does
``logger_level_msg`` of ``LCDEx`` objects, for example — each
logged message will relate which module wrote it.

The following example illustrates the general technique:

    >>> from lcd import LCDEx
    >>> import logging
    >>> lcd_ex = LCDEx(attach_handlers_to_root=True)
    >>> lcd_ex.add_stdout_handler('con', formatter='logger_level_msg')
    >>> lcd_ex.config()

    >>> logging.getLogger().warning("Look out!")
    root                : WARNING : Look out!
    >>> logging.getLogger('my_submodule').warning("Something wasn't right.")
    my_submodule        : WARNING : Something's was not right.
    >>> logging.getLogger('your_submodule').error("Uh oh, there was an error.")
    your_submodule      : ERROR   : Uh oh, there was an error.


--------------------------------------------------

.. _tr-add-non-root:

Configuring and using non-root loggers
----------------------------------------------

Reasons to do so:

    * in a particular module or package, you want to use a different loglevel
      from that of the root logger, using the same handlers as the root (& so,
      writing to the same destination(s));

    * you want to write to destinations other than those of the root,
      either instead of or in addition to those.


.. _tr-config-non-root-propagate:

A propagating non-root logger
+++++++++++++++++++++++++++++++++++++++++++++++

.. todo:: this.

One which propagates. There are two possibilities:

    1. the non-root logger has no handlers attached;
    2. the non-root logger has handlers attached.

Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<<<<< TODO >>>>> 

How-to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<<<<< TODO >>>>> 


.. _tr-config-discrete-non-root:

A "discrete" non-root logger
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

In this example we use two loggers: the root, and another logger that's
"discrete" from the root, and indeed from any ancestor logger, in the sense
that:

    * it doesn't share any handlers with any ancestor, and
    * it doesn't propagate to any ancestor.

As the root is an ancestor of every logger, in particular we'll require that
the added logger should *not* attach its handlers to the root, and that it
should not "propagate" to its parent (the root, in this example).


Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Root logger with a ``stderr`` console handler and a file handler,
at their respective `lcd` default loglevels ``'WARNING'`` and ``'NOTSET'``;

a discrete logger, named let's say ``'extra'``, with loglevel ''`DEBUG`'',
which will write to a different file using a handler at default loglevel
``'NOTSET'``.

How-to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start with a ``LCDEx`` that uses standard (non-locking) stream
and file handlers; use root loglevel ``'DEBUG'``; put logfiles in the ``_log/``
subdirectory of the current directory::

    import logging
    from lcd import LCDEx


    lcd_ex = LCDEx(log_path='_log/',
                   root_level='DEBUG',
                   attach_handlers_to_root=True)

Set up the root logger with a ``stderr`` console handler and a file handler,
at their respective default loglevels ``'WARNING'`` and ``'NOTSET'``::

    lcd_ex.add_stderr_handler('console', formatter='minimal')
    lcd_ex.add_file_handler('root_fh',
                            filename='root.log',
                            formatter='logger_level_msg')

Add an ``'extra'`` logger, with loglevel ''`DEBUG`'', which will write to a
different file using a handler at default loglevel ``'NOTSET'``.
Note the use of parameters ``attach_to_root`` and ``propagate``:

    * in the ``add_file_handler`` call, passing ``attach_to_root=False`` ensures
      that this handler *won't* be attached to the root logger, overriding the
      ``lcd_ex`` default value established by ``attach_handlers_to_root=True``
      above;

    * in the ``add_logger`` call, ``propagate=False`` ensures that messages
      logged by ``'extra'`` don't also write to the root and its handlers:

.. code::

        lcd_ex.add_file_handler('extra_fh',
                                filename='extra.log',
                                formatter='logger_level_msg',
                                attach_to_root=False)
        lcd_ex.add_logger('extra',
                          handlers=['extra_fh'],
                          level='DEBUG',
                          propagate=False)

Finally, call ``config()`` to create actual objects of `logging` types —
``logging.Formatter``, ``logging.Logger``, etc. ::

    lcd_ex.config()

Now ``lcd_ex`` is actually no longer needed (we don't do 'incremental'
configuration, but then, arguably, neither does `logging`).

To use the loggers, access them by name::

    # 'extra' writes "Hi there" to file `_LOG/extra.log`:
    logging.getLogger('extra').warning("Hi there.")

    # Root writes "UH OH" to `stderr` and to `_LOG/root.log`:
    logging.getLogger().error("UH OH")

    # Root writes "ho hum" to `_LOG/root.log` only:
    logging.getLogger().debug("ho hum")

**Exercise**: Verify the claimed effects of the ``attach_to_root`` and
``propagate`` parameters in the two calls that configure the ``'extra_fh'``
handler and the ``'extra'`` logger.

    1. Comment out ``attach_to_root=False`` from the ``add_file_handler`` call
       for ``'extra_fh'``.

       Now, ``'extra_fh'`` is a handler of the root logger *too*, so
       it logs its messages ``"UH OH"`` and ``"ho hum"`` to ``_LOG/extra.log``,
       as well as to ``root.log`` and ``stderr`` as before.

       ``_LOG/root.log`` contains::

            root                : ERROR   : UH OH
            root                : DEBUG   : ho hum

       ``_LOG/extra.log`` contains::

            extra               : WARNING : Hi there.
            root                : ERROR   : UH OH
            root                : DEBUG   : ho hum

       ``stderr`` output::

            UH OH

    2. Uncomment ``attach_to_root=False`` in the ``add_file_handler`` call,
       and comment out ``propagate=False`` from the ``add_logger`` call.

       Now, ``'extra'`` writes to the root's handlers as well as its own,
       so it logs a warning ``"Hi there."`` to both ``stderr`` and
       ``_LOG/root.log``.

       ``_LOG/root.log`` contains::

            extra               : WARNING : Hi there.
            root                : ERROR   : UH OH
            root                : DEBUG   : ho hum

       ``_LOG/extra.log`` contains::

            extra               : WARNING : Hi there.

       ``stderr`` output::

            Hi there.
            UH OH


.. _tr-propagate-docs:

.. index:: Logger.propagate property
.. index:: Propagation — best practices
.. index:: Placement of handlers when using multiple loggers — best practices

.. topic:: Best practices for propagation and handler placement

    According to the documentation for
    `Logger.propagate <https://docs.python.org/3/library/logging.html#logging.Logger.propagate>`_,


    | if [a logger's ``propagate`` property] evaluates to true [the default],
    | events logged to this logger will be passed to the handlers of higher level
    | (ancestor) loggers, in addition to any handlers attached to this logger.
    | Messages are passed directly to the ancestor loggers’ handlers - neither
    | the level nor filters of the ancestor loggers in question are considered.

    |br|
    This suggests that truly intricate, and no doubt surprising, configurations
    can be achieved using propagation and fussy placements of handlers on
    loggers. The **Note** at the end of the above link clearly states best
    practice:

    | If you attach a handler to a logger and one or more of its ancestors,
    | it may emit the same record multiple times. In general, you should not
    | need to attach a handler to more than one logger - if you just attach it
    | to the appropriate logger which is highest in the logger hierarchy, then
    | it will see all events logged by all descendant loggers, provided that
    | their propagate setting is left set to True. A common scenario is to
    | attach handlers only to the root logger, and to let propagation take care
    | of the rest.

--------------------------------------------------

.. _using-lcd-with-django:

Using `lcd` with `Django`
------------------------------------

.. todo::

    This needs mention

    Django uses logging config dicts, & it's path of least resistance
    suggests using a big static dict
    via a LOGGING variable in ``settings.py``.

    ..note :: It would be great if LOGGING could be a callable,
        as the other logging-related setting ______ can be.
        That way, you could specify a callable (no args, say) that just returns
        a logging config dict.

    See blah for info:
        https://docs.djangoproject.com/en/1.9/topics/logging/

        also

        https://docs.djangoproject.com/en/1.9/releases/1.9/#default-logging-changes-19

    Illustrate how to use `lcd` with Django. In ``settings.py``:

    .. code::

        from mystuff import build_lcd
        LOGGING = build_lcd()

    Here, `build_lcd` is a function you supply which builds a logging
    config dict but doesn't call its ``config`` method. Django will add its
    logging specifications to the ``LOGGING`` dict and then pass that to
    ``logging.config.dictConfig``.

    From https://docs.djangoproject.com/en/1.9/topics/logging/:

        If the disable_existing_loggers key in the LOGGING dictConfig is set to
        ``True`` (which is the default) then all loggers from the default
        configuration will be disabled. Disabled loggers are not the same as
        removed; the logger will still exist, but will silently discard anything
        logged to it, not even propagating entries to a parent logger. Thus you
        should be very careful using ``'disable_existing_loggers': True``; it’s
        probably not what you want. Instead, you can set
        ``disable_existing_loggers`` to ``False`` and redefine some or all of
        the default loggers; or you can set ``LOGGING_CONFIG`` to ``None`` and
        handle logging config yourself.


--------------------------------------------------

.. _error- checking:

Error-checking: the ``warn`` property (default: False)
-----------------------------------------------------------

<<<<< TODO >>>>>


--------------------------------------------------

.. _tr-rot-fh:

Using a rotating file handler
------------------------------------

<<<<< TODO >>>>> 

--------------------------------------------------


.. _tr-mp:

Multiprocessing — two approaches
----------------------------------------------
Refer to "multiple handlers logging to the same file" (sic)
PROVIDE A LINK, and/or quote from it. That section of the docs discusses
three approaches:

    1. one based on ``SocketHandler``
    2. locking versions of handlers, which our locking handlers implement
    3. (*Python 3 only*) using a ``QueueHandler`` in each process, all writing
       to a common Queue, and then either a ``QueueListener``
       or a dedicated thread in another process (e.g. the main one)
       to extract ``LogRecord``\s from the queue and log them.

**Note**: the third approach is unavailable in Python 2, as the class
``QueueHandler`` is Python 3 only.

In this section we'll discuss the second and third approaches.

.. _basic-mproc-situation:

.. topic:: Basic situation and challenge

    We have some amount of work to do, and the code that performs it uses logging.
    Let's say there are :math:`L` many loggers used:

        .. math::

            logger_1, \cdots, logger_i, \cdots, logger_L,

    Each logger :math:`logger_i` is denoted by some name :math:`name_i`,
    and has some intended handlers

        .. math::

            handler_{i, j} \quad (j < n_i).

    Later, we notice that the work can be parallelized: we can partition it into
    chunks which can be worked on simultaneously and then recombined.
    We put the code that performs the work into a function, and spawn :math:`N`
    worker processes

    .. math::

        P_1, ..., P_k, ... P_N,

    each of which runs that function on a discrete chunk of the data. The worker
    processes are basically homogeneous, but for their distinct PIDs, names,
    and the ranges of data they operate on. Now, each worker process :math:`P_k`
    uses all the loggers :math:`logger_i, i < L`. All the loggers and handlers
    have different instances in different processes; however, all the handler
    destinations remain unique. Somehow, we have to serialize writing to single
    destinations from multiple concurrent processes.

.. topic:: Two solutions

    In the approach provided natively by `lcd`, serialization occurs at the handler
    level, using the package's simple "locking handler" classes. Before
    an instance of a locking handler writes to its destination, it acquires
    a lock (*shared by all instances* of the handler), which it releases when done;
    attempts by other instances to write concurrently will block until the lock
    is released by the handler that "got there first".

    The queue-based approach is an important and sometimes more performant
    alternative. Using an explicit shared queue and a layer of indirection,
    this approach serializes messages early in their lifecycle.
    Each process merely enqueues logged messages to the shared queue,
    in the form of ``LogRecord``\s. The actual writing of the message to the intended destinations
    occurs later, in a dedicated *logging thread* of a non-worker process.
    That thread pulls logging records off the queue and *handles* them, so that
    messages are finally dispatched to their intended handlers and destinations.
    The `logging` package's ``QueueHandler`` class makes all this possible.


.. note:: A pair of examples using the two approaches to solve the same problem:

    * ``mproc_approach__locking_handlers.py`` uses locking handlers,
    * ``mproc_approach__queue_handler_logging_thread.py`` uses a queue and logging thread.

    In these examples, the handlers only write to files, and performance of
    the two approaches is about the same, with the queue-based approach slightly
    faster (though YMMV).

.. _mp-locking-handlers:

Using locking handlers
+++++++++++++++++++++++++

(MP blather)

For a particular ``LCDEx``, there are two possibilities:

.. topic:: locking handlers used by default
    on every ``add_*_handler`` method call

    ``locking=True`` was passed to constructor

vs

.. topic:: standard handlers used by default
    on every ``add_*_handler`` method call

    ``locking=False`` was passed to constructor

    When you add (specs for) a handler using an ``add_*_handler`` method,
    pass ``locking=True`` to the method in order for the handler to be locking.

.. note::
    All but one of the multiprocessing examples use locking handlers.


.. _tr-mp-console:

Using a locking console handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<<<<< TODO >>>>> 

.. _tr-mp-fh:

Using a locking file handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<<<<< TODO >>>>> 

.. _tr-mp-rot-fh:

Using a locking rotating file handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<<<<< TODO >>>>> 

Using a locking syslog handler [?????]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<<<<< TODO [?????] >>>>>

.. _mp-queue-and-logging-thread:

Using QueueHandlers (*Python 3 only*)
++++++++++++++++++++++++++++++++++++++++++

The queue based approach serializes logged messages as soon as possible,
moving the actual writing of messages out of the worker processes.
Worker processes merely enqueue messages, with context, onto a common queue.
The real handlers don't run in the worker processes: they run in
a dedicated thread of the main process, where records are dequeued from that
common queue and handled in the ways you intend.

When a worker process :math:`P_k` logs a message using one of the loggers
:math:`logger_i`, none of the "real", intended handlers of that logger
executes in :math:`P_k`. Instead, the message, in the form
of a ``logging.LogRecord``, is put on a ``Queue`` object which all
the processes share. The enqueued record contains all information required to
write it later, even in another process. This is all achieved by a simple
logging configuration that uses `logging`\'s ``QueueHandler`` class.

In a dedicated thread in another process — the main process, let's assume —
a tight loop polls the shared queue and pulls records from it. Each record
contains context information from the originating process :math:`P_k`,
including the logger's name, the message's loglevel, the process name of
:math:`P_k` — values for the keys that can occur in format strings. The thread
uses this information to dispatch the record via the originating logger,
and finally the intended handlers execute. This setup too is easily achieved
with an appropriate logging configuration.

.. figure:: mproc_queue_paradigm.png

    Multiprocess logging with a queue

This design gives better performance, especially for blocking, slow handlers
(SMTP, for example). Generally, the worker processes have better things to do
than wait for emails to be successfully sent, so we relieve them of such
extraneous burdens.

Handling all logged messages in a dedicated thread (of a non-worker process)
confers additional benefits:

* the UI won't stutter or temporarily freeze
  whenever a slow (and blocking) handler runs;
* the main thread can do other useful things.

The queue-based approach confers these same benefits even in single-processing
situations. The example ``queue_handler_listener.py`` illustrates this, using
the logging package's ``QueueListener`` instead of a logging-thread.
``QueueListener``\s encapsulate setup and teardown of a logging thread,
and the proper handling of queued messages. It's unfortunate that they're
an awkward fit for static configuration.

.. topic:: Aside: ``QueueListeners`` and static configuration

    It's awkward to use a ``QueueListener`` with static configuration.
    Once it has been created, a ``QueueListener`` has to be stopped and started,
    using its ``stop`` and ``start`` methods. If we could statically specify a
    ``QueueListener``, somehow we have to obtain a reference it after configuring
    logging, in order to call these methods.

    Furthermore, a ``QueueListener`` must be initialized/constructed with one
    or more ``QueueHandler``\s -- actual handler objects. Of course, these don't
    exist before configuration, and then the names we gave them in configuration
    have disappeared. As we've noted elsewhere,
    handler objects are anonymous, so the only way to obtain references to the
    ``QueueHandler``\s is a bit disappointing (filter the handlers of some logger
    with ``isinstance(handler, QueueHandler)``). The example
    ``queue_handler_listener.py`` demonstrates this in action.


Worker process configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The main process creates a common queue, then spawns the worker processes
:math:`P_k`, passing the queue to each one. The worker processes *use, but
do not configure* the intended loggers :math:`logger_i`. In the logging
configuration of the worker processes, these loggers have *no handlers*. Thus,
because of inheritance, all messages are actually logged by their common
ancestor, the root logger. The root is equipped with a single handler:
a ``QueueHandler``, which puts messages on a queue it's initialized with.

At startup, every worker process configures logging in this simple way:

.. code::

    def worker_config_logging(q: Queue):
        d = LCDEx(root_level='DEBUG')
        d.add_queue_handler('qhandler', attach_to_root=True, queue=q)
        d.config()

*logging thread*/main process configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The logging thread does one thing: dispatch logged messages to their ultimate
destinations as they arrive. Before the main process creates the logging thread,
it configures logging as you really intend.
The configuration used here is essentially what you would use in
the locking handlers approach (but with ``locking=False``).
The logging configuration specifies all the intended loggers :math:`logger_i`,
after specifying, for each logger, all of its intended handlers
:math:`handler_{i, j}, j < n_i` and any formatters they use.
As a result, the 'real' handlers finally execute.

Here's what the logging thread does:

.. code::

    def logging_thread(q):
        while True:
            record = q.get()
            if record is None:
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)

--------------------------------------------------

.. _tr-filters:

Filters
--------

There are two principle kinds of filters: instances of ``logging.Filter``,
and callables of signature ``LogRecord`` -> ``bool``. `lcd` provides a pair
of convenience methods ``add_class_filter`` and ``add_callable_filter``
which are somewhat easier to use than its lower-level ``add_filter`` method.

``logging.Filter`` objects have a ``filter(record)`` method
which takes a ``logging.LogRecord`` and returns ``bool``.

In Python 2, the `logging` module imposes a fussy requirement on callables
that can be used as filters, which Python 3 implementation of `logging` removes.
``add_callable_filter`` addresses the Python 2 requirement, providing a single
interface for adding callable filters that works in both Python versions.

.. _filter-setup:

Defining filters
++++++++++++++++++++++++++++++++

Here are a couple of examples of filters, both of which suppress
certain kinds of messages. Each has the side effect of incrementing
a distinct global variable::

    _info_count = 0
    _debug_count = 0

Classic filters are subclasses of ``logging.Filter``:

.. code::

    class CountInfoSquelchOdd(logging.Filter):
        def filter(self_, record):
            """Suppress odd-numbered messages (records) whose level == INFO,
            where the "first" message is the 0-th hence is even-numbered.

            :param self_: "self" for the CountInfo object (unused)
            :param record: logging.LogRecord
            :return: bool -- True ==> let record through, False ==> squelch
            """
            global _info_count
            if record.levelno == logging.INFO:
                _info_count += 1
                return _info_count % 2
            else:
                return True

A filter can also be a function:

.. code::

    def count_debug_allow_2(record):
        """
        :param record: ``logging.LogRecord``
        :return: ``bool`` -- True ==> let record through, False ==> squelch
        """
        global _debug_count
        if record.levelno == logging.DEBUG:
            _debug_count += 1
            return _debug_count <= 2
        else:
            return True


.. _tr-filters-logger:

Filters on the root logger
+++++++++++++++++++++++++++++

Let's configure the root logger to use both filters shown above::

    lcd_ex = LCDEx(
        attach_handlers_to_root=True,
        root_level='DEBUG')

    lcd_ex.add_stdout_handler(
        'console',
        level='DEBUG',
        formatter='level_msg')

    lcd_ex.add_callable_filter('count_d', count_debug_allow_2)
    lcd_ex.add_class_filter('count_i', CountInfoSquelchOdd)

    lcd_ex.attach_root_filters('count_d', 'count_i')

    lcd_ex.config()

Now use the root logger::

    import logging
    root = logging.getLogger()

    # Py2: use u"Hi 1", etc.
    for i in range(5):
        root.debug(str(i))
        root.info(str(i))

    print("_debug_count:", _debug_count)
    print("_info_count:", _info_count)

This passage writes the following to ``stdout``::

    DEBUG   : 0
    INFO    : 0
    DEBUG   : 1
    INFO    : 2
    INFO    : 4
    _debug_count: 5
    _info_count: 5

.. note::
    This example **is** the test ``test_add_xxx_filter.py``, with little
    modification.


Filters on a non-root logger
+++++++++++++++++++++++++++++

Attaching the example filters to a non-root logger ``'mylogger'`` requires just
one change: instead of using ``attach_root_filters('count_d', 'count_i')`` to
attach the filters to the root logger, now we have to attach them to an
arbitrary logger. This can be accomplished in two ways:

1. Attach the filters when calling ``add_logger`` for ``'mylogger'``, using the
   ``filters`` keyword parameter::

    lcd_ex.add_logger('mylogger',
                      filters=['count_d', 'count_i'],
                      ...
                     )

2. Add the logger with ``add_logger``, without using the ``filters`` parameter::

    lcd_ex.add_logger('mylogger', ... )

   and then attach filters to it with ``attach_logger_filters``::

    lcd_ex.attach_logger_filters('mylogger',
                                 'count_d', 'count_i')

.. _tr-filters-handler:

Filters on a handler
+++++++++++++++++++++++++++++

There are two ways to attach filters to a handler:

1. Attach the filters in the same method call that adds the handler.
   Use the ``filters`` keyword parameter to **any** ``add_*_handler`` method.
   All such methods funnel through ``LCD.add_handler``. The
   value of the ``filters`` parameter can be either the name of a single filter
   (a ``str``) or a sequence (list, tuple, etc.) of names of filters.

   For example, using our two example filters, each of the following method
   calls adds a handler with just the ``'count_d'`` filter attached::

    lcd_ex.add_stderr_handler('con-err',
                                      filters='count_d')
    lcd_ex.add_file_handler('fh',
                            filename='some-logfile.log',
                            filters=['count_d'])

   The following statement adds a rotating file handler with both filters
   attached::

    lcd_ex.add_rotating_file_handler('rfh',
                                     filename='some-rotating-logfile.log',
                                     max_bytes=1024,
                                     backup_count=5,
                                     filters=['count_i', 'count_d'])

2. Add the handler using any ``add_*_handler`` method, then use
   ``add_handler_filters`` to attach filters to the handler. For example::

    lcd_ex.add_file_handler('myhandler',
                            filename='mylogfile.log')
    lcd_ex.attach_handler_filters('myhandler',
                                  'count_d', 'count_i')


.. index:: Filters -- passing initialization data

.. _passing-initialization-data-to-a-filter:

Passing initialization data to a filter
+++++++++++++++++++++++++++++++++++++++++++++
Blah blah

    .. todo::
        Filter examples:

            Class Filter    that's initialized with some data:
                            using keyword parameters for initialization

            Callable filter  "    "     "       "         "     "


Class filter
~~~~~~~~~~~~~~~~~~~
<<<<< TODO >>>>>

Callable filter
~~~~~~~~~~~~~~~~~~~
<<<<< TODO >>>>>
    (Cool new feature of ``add_callable_filter``, that you can do this)


.. index:: Filters -- passing dynamic data

.. _passing-dynamic-data-to-a-filter:

Passing dynamic data to a filter
++++++++++++++++++++++++++++++++++++

Sometimes you may want to pass a reference dynamic data to a filter, whose
value may be different from one filter call to the next. A typical approach
would be to wrap such data in a list or dict, as in the following code which
uses a list:

    >>> class A():
    ...     def __init__(self, list1=None):
    ...         self.list1 = list1
    ...
    ...     def method(self):
    ...         print(self.list1[0])

    >>> data_wrapper = [17]
    >>> a = A(list1=data_wrapper)
    >>> a.method()
    17
    >>> data_wrapper[0] = 101
    >>> a.method()
    101

This will not work with logging configuration.

Configuring logging "freezes" lists and dicts in the logging config dict
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While you're still building a logging config dict, the dict for a filter will
reflect changes to any data that's accessible through dict or list references
you've passed. For example,

    >>> def my_filter_fn(record, list1=None):
    ...     assert list1
    ...     print(list1[0])
    ...     return list1[0] > 100

    >>> data_wrapper = [17]
    >>> lcdx = LCDEx(attach_handlers_to_root=True, root_level='DEBUG')
    >>> lcdx.add_stdout_handler('con', formatter='minimal', level='DEBUG')
    >>> lcdx.add_callable_filter('callable-filter',
    ...                          my_filter_fn,
    ...                          list1=data_wrapper)
    >>> lcdx.attach_root_filters('callable-filter')
    >>> lcdx.filters['callable-filter']['list1']
    [17]
    >>> data_wrapper[0] = 21
    >>> lcdx.filters['callable-filter']['list1']
    [21]

However, once you configure logging, any such live references are broken,
because the values in the dict are copied. Let's confirm this.
First, configure logging with the dict we've built:

    >>> lcdx.config()

Now log something. The filter prints the value of ``list1[0]``, which is ``21``;
thus it returns ``False``, so no message is logged:

    >>> logging.getLogger().debug("data_wrapper = %r" % data_wrapper)
    21

Now change the value of ``data_wrapper[0]``:

    >>> data_wrapper[0] = 101

Prior to configuration, the filter's ``list1`` referred to ``data_wrapper``;
but that's no longer true: ``list1[0]`` is still ``21``, not `101`, so the
filter still returns ``False``:

    >>> logging.getLogger().debug("data_wrapper = %r" % data_wrapper)
    21

Successfully passing dynamic data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The moral of the story: if you want to pass dynamic data to a filter, you
can't use a list or dict as a container (nor, of course, a tuple). The
following example shows a successful strategy, using a simple ad-hoc class
as a container:

    >>> class DataWrapper():
    ...     def __init__(self, data=None):  self.data = data
    ...     def __str__(self):              return "%r" % self.data

    >>> def my_filter_fn(record, data_wrapper=None):
    ...     assert data_wrapper
    ...     print(data_wrapper)
    ...     return isinstance(data_wrapper.data, int) and data_wrapper.data > 100

    >>> dw = DataWrapper(17)

    >>> lcdx = LCDEx(attach_handlers_to_root=True, root_level='DEBUG')
    >>> lcdx.add_stdout_handler('con', formatter='minimal', level='DEBUG')
    >>> lcdx.add_callable_filter('callable-filter',
    ...                          my_filter_fn,
    ...                          data_wrapper=dw)
    >>> lcdx.attach_root_filters('callable-filter')
    >>> lcdx.filters['callable-filter']['data_wrapper'])
    17
    >>> dw.data = 21
    >>> lcdx.filters['callable-filter']['data_wrapper'])
    21

    >>> lcdx.config()

    >>> # filter prints 21 and returns False:
    >>> # in the filter, data_wrapper.data == 21
    >>> logging.getLogger().debug("dw = %s" % dw)
    21
    dw.data = 101
    >>> # In the filter, data_wrapper.data == 101,
    >>> #  so message is logged:
    logging.getLogger().debug("dw = %s" % dw)
    101
    dw = 101

Of course, you could pass a data-returning callable rather than a container.

----------------------------------

.. _config-abc:

Using ``LCDBuilderABC``
-------------------------------

A single ``LCDEx`` can be passed around to different "areas"
of a program, each area contributing specifications of its desired formatters,
filters, handlers and loggers. The ``LCDBuilderABC`` class provides a
framework that automates this approach: each area of a program need only
define a ``LCDBuilderABC`` subclass and override its method
``add_to_lcd(lcd)``, where it contributes its specifications by calling
methods on ``lcd``.

The :ref:`LCDBuilderABC` documentation describes how that class and its two
methods operate. The test ``tests/test_configurator.py`` exemplifies using
the class to configure logging across multiple modules.

    <<<<< TODO -- more... how much more? >>>>>
    <<<<< Walk through code? Simplified further if possible >>>>>
    <<<<< Go look...  >>>>>

.. _using-other-logging-handler-classes:

Using other `logging` ``Handler`` classes
--------------------------------------------

.. todo::
    How you say in Inglese? --

The `logging` package defines about a dozen handler classes — subclasses of
``logging.Handler`` — in the modules ``logging`` and ``logging.handlers``.
``logging`` defines the basic handler classes ... TODO ...

which log to more exotic destinations than just files
and the console.

— use ``add_handler``, using keyword arguments to specify
class-specific key/value pairs, and specifying the appropriate handler class
with the ``class_`` keyword.

.. _null-handler:

NullHandler
+++++++++++++++++++++++++++++
class: ``logging.NullHandler``

.. _smtp-handler:

SMTPHandler
+++++++++++++++++++++++++++++
class: ``logging.handlers.NullHandler``

docs: `<https://docs.python.org/3/library/logging.handlers.html#module-logging.handlers>`_

Use the queue handler approach to send emails from a thread other than the main
one (and other than the UI thread).  Sending an email can take a comparatively
long time, so you'll want to do that "in the background", and not have other
processes, or the UI, block and stutter whenever an email is sent.




.. _smtp-handler-one:

Using a single SMTPHandler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: comment on the following code
    Commentary on example ``SMTP_handler_just_one.py``

.. code::

    from lcd import LCDEx
    from _smtp_credentials import *

    # for testing/trying the example
    TEST_TO_ADDRESS = FROM_ADDRESS

    # root, console handler levels: WARNING.
    lcdx = LCDEx(attach_handlers_to_root=True)
    lcdx.add_stderr_handler('con-err',
                                    formatter='minimal'
    ).add_email_handler('email-handler',
        level='ERROR',
        formatter='time_logger_level_msg',
        # SMTPHandler-specific kwargs:
        mailhost='smtp.gmail.com',
        fromaddr=FROM_ADDRESS,
        toaddrs=[TEST_TO_ADDRESS, 'uh.oh@kludge.ly'], # string or list of strings
        subject='Alert from SMTPHandler',
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD
    )

    lcdx.config()

    root = logging.getLogger()
    root.debug("1.")        # not logged (loglevel too low)
    root.info("2.")         # ditto
    root.warning("3.")      # logged to console
    root.error("4.")        # logged to console, emailed
    root.critical("5.")     # ditto

.. _smtp-handlers-two-error-and-critical:

Using two SMTPHandlers, one filtered
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comment on the example ``SMTP_handler_two.py``

.. todo:: comment on the following code

.. code::

    from lcd import LCDEx

    from _smtp_credentials import *

    # for testing/trying it the example
    TEST_TO_ADDRESS = FROM_ADDRESS


    def add_email_handler_to_lcd(
                         lcdx,          # *
                         handler_name,
                         level,
                         toaddrs,        # string or list of strings
                         subject,
                         filters=()):
        """Factor out calls to ``add_email_handler``.
        """
        lcdx.add_email_handler(
            handler_name,
            level=level,
            filters=filters,

            toaddrs=toaddrs,
            subject=subject,

            formatter='time_logger_level_msg',
            fromaddr=FROM_ADDRESS,
            mailhost=SMTP_SERVER,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD
        )

    def filter_error_only(record):
        "Let only ERROR messages through"
        return record.levelname  == 'ERROR'


    def build_lcd():
        lcdx = LCDEx(attach_handlers_to_root=True)
        lcdx.add_stderr_handler('con-err', formatter='level_msg')
        # root, console handler levels: WARNING.

        # Add TWO SMTPHandlers, one for each level ERROR and CRITICAL,
        #    which will email technical staff with logged messages of levels >= ERROR.
        # We use a filter to make the first handler squelch CRITICAL messages:
        lcdx.add_callable_filter("filter-error-only", filter_error_only)

        # TEST_TO_ADDRESS included just for testing/trying out the example
        basic_toaddrs = [TEST_TO_ADDRESS, 'problems@kludge.ly']

        # add error-only SMTP handler
        add_email_handler_to_lcd(
                         lcdx,
                         'email-error',
                         level='ERROR',
                         toaddrs=basic_toaddrs,
                         subject='ERROR (Alert from SMTPHandler)',
                         filters=['filter-error-only'])
        # add critical-only SMTP handler
        add_email_handler_to_lcd(
                         lcdx,
                         'email-critical',
                         level='CRITICAL',
                         toaddrs=basic_toaddrs + ['cto@kludge.ly'],
                         subject='CRITICAL (Alert from SMTPHandler)')
        lcdx.config()

    # -----------------------------------------

    build_lcd()

    root = logging.getLogger()
    root.warning("Be careful")                  # logged to console
    root.error("Something bad just happened")   # logged to console, emailed
    root.critical("Time to restart")            # ditto

.. _smtp-handler-custom-keywords-in-formatter-filter-adds-info:

SMTPHandler logging custom fields using a custom formatter and filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo::
    Use `lcd` to realize the example described in:

            https://docs.python.org/3/howto/logging-cookbook.html#using-filters-to-impart-contextual-information

