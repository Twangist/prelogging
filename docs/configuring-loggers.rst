Configuring Loggers
=======================================================

We have already seen examples of how easy it can be to configure the root logger
— for example, with both a console handler and a file handler, as in the
:ref:`overview<example-overview-config>`.

This chapter is mainly concerned with configuring non-root loggers. We'll
begin by considering the special case of "configuring" non-root loggers by not
configuring them at all, so that the root does all the work via propagation.

For simplicity the examples in this chapter use the root logger and non-root loggers,
but they can be adapted to the more general situation of a non-propagating
logger with handlers, and its descendants.


.. include:: _global.rst

* Configuring non-root loggers by propagation to the root
    .. hlist::
        :columns: 3

        * :ref:`config-root-use-children`

* Configuring non-root loggers; using root and non-root loggers together
    .. hlist::
        :columns: 3

        * :ref:`example-discrete-nonroot-logger`
        * :ref:`propagate-docs-best-practices`

--------------------------------------------------


.. _config-root-use-children:

Using non-root loggers without configuring them
-------------------------------------------------------

A common, useful approach is to attach handlers only to the root logger,
and then have each module log messages using ``logging.getLogger(__name__)``.
These "child" loggers require no configuration; they use the handlers
of the root because, by default, loggers are created with ``propagate=True``
(and with ``level='NOTSET'``).

If the formatters of the handlers include the logger name — as the formatter
preset ``logger_level_msg`` does, for example — each logged message will state
which logger wrote it.

The following example illustrates the general technique:

    >>> from prelogging import LCDict
    >>> import logging
    >>> lcd = LCDict(attach_handlers_to_root=True)
    >>> lcd.add_stdout_handler('con', formatter='logger_level_msg')
    >>> lcd.config()

    >>> logging.getLogger().warning("Look out!")
    root                : WARNING : Look out!
    >>> logging.getLogger('my_submodule').warning("Something wasn't right.")
    my_submodule        : WARNING : Something's wasn't right.
    >>> logging.getLogger('your_submodule').error("Uh oh, there was an error.")
    your_submodule      : ERROR   : Uh oh, there was an error.

--------------------------------------------------

.. _add-non-root:

Configuring and using non-root loggers
----------------------------------------------

In the previous section we saw one common configuration of non-root loggers.
Other configurations are possible and sometimes desirable:

    * you want the logger for a module or package to have a different loglevel
      from that of the root, but to use the same handlers as the root (thus,
      it will write to the same destination(s));

    * you want to write to destinations other than those of the root,
      either instead of or in addition to those.

The first case is easily achieved simply by setting the loglevel of the non-root
logger as desired, giving it no handlers; propagation takes care of the rest
(a logger's ``propagate`` property is, by default, true).

The second case has many variations, depending upon whether the non-root logger
propagates or not.  We consider a non-propagating example, where the
non-root logger is totally "walled off" from the root logger. Variations will
be easy to devise and configure.

.. _example-discrete-nonroot-logger:

Example: A "discrete" non-root logger
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

* root logger with a ``stderr`` console handler at loglevel ``WARNING``,
  and a file handler at default loglevel ``NOTSET``;

* a discrete logger, named let's say ``'extra'``, with loglevel ``DEBUG``,
  which will write to a different file using a handler at default loglevel
  ``NOTSET``;
* logfiles should be in the ``_log/`` subdirectory of the current directory.

How-to
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start with an ``LCDict`` that uses standard (non-locking) stream
and file handlers; use root loglevel ``'DEBUG'``; set ``log_path`` as required::

    import logging
    from prelogging import LCDict


    lcd = LCDict(log_path='_log/',
                 root_level='DEBUG',
                 attach_handlers_to_root=True)

Set up the root logger with a ``stderr`` console handler at loglevel 'WARNING',
and a file handler at its default loglevel 'NOTSET'::

    lcd.add_stderr_handler('console',
                           level='WARNING',
                           formatter='msg'
    ).add_file_handler('root_fh',
                       filename='root.log',
                       formatter='logger_level_msg')

Add an ``'extra'`` logger, with loglevel ``DEBUG``, which will write to a
different file using a handler at default loglevel ``NOTSET``.
Note the use of parameters ``attach_to_root`` and ``propagate``:

    * in the ``add_file_handler`` call, passing ``attach_to_root=False`` ensures
      that this handler *won't* be attached to the root logger, overriding the
      ``lcd`` default value established by ``attach_handlers_to_root=True``
      above;

    * in the ``add_logger`` call, ``propagate=False`` ensures that messages
      logged by ``'extra'`` don't also bubble up to the root and its handlers:

.. code::

        lcd.add_file_handler('extra_fh',
                             filename='extra.log',
                             formatter='logger_level_msg',
                             attach_to_root=False
        ).add_logger('extra',
                     handlers=['extra_fh'],
                     level='DEBUG',
                     propagate=False)

Finally, call ``config()`` to create actual objects of `logging` types —
``logging.Formatter``, ``logging.Logger``, etc. ::

    lcd.config()

Now ``lcd`` is actually no longer needed (we don't do 'incremental'
configuration, but then, arguably, neither does `logging`).

To use the loggers, access them by name::

    # 'extra' writes "Hi there" to file `_log/extra.log`:
    logging.getLogger('extra').warning("Hi there.")

    # Root writes "UH OH" to `stderr` and to `_log/root.log`:
    logging.getLogger().error("UH OH")

    # Root writes "ho hum" to `_log/root.log` only:
    logging.getLogger().debug("ho hum")

.. index:: Exercise on ``propagate`` and ``attach_to_root``

**Exercise**: Verify the claimed effects of the ``attach_to_root`` and
``propagate`` parameters in the two calls that configure the ``'extra_fh'``
handler and the ``'extra'`` logger.

    1. Comment out ``attach_to_root=False`` from the ``add_file_handler`` call
       for ``'extra_fh'``.

       Now, ``'extra_fh'`` is a handler of the root logger *too*, so
       it logs its messages ``"UH OH"`` and ``"ho hum"`` to ``_log/extra.log``,
       as well as to ``root.log`` and ``stderr`` as before.

       ``_log/root.log`` contains::

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
       ``_log/root.log``.

       ``_log/root.log`` contains::

            extra               : WARNING : Hi there.
            root                : ERROR   : UH OH
            root                : DEBUG   : ho hum

       ``_log/extra.log`` contains::

            extra               : WARNING : Hi there.

       ``stderr`` output::

            Hi there.
            UH OH


.. index:: Logger.propagate property
.. index:: Propagation — best practices
.. index:: Placement of handlers when using multiple loggers — best practices

-------------------------------------------

.. _propagate-docs-best-practices:

Best practices for propagation and handler placement
------------------------------------------------------
The examples in this chapter, and the preceding Exercise, have hopefully
conveyed the significance of propagation and the importance of "right"
handler placement. Now is a good time to reflect further on these matters.

According to the documentation for `Logger.propagate <https://docs.python.org/3/library/logging.html#logging.Logger.propagate>`_,


    | if [a logger's ``propagate`` property] evaluates to true [the default],
    | events logged to this logger will be passed to the handlers of higher level
    | (ancestor) loggers, in addition to any handlers attached to this logger.
    | Messages are passed directly to the ancestor loggers’ handlers - neither
    | the level nor filters of the ancestor loggers in question are considered.

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

