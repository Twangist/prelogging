.. include:: _global.rst

.. _guide-to-examples:

Guide to Examples
========================

The `prelogging` distribution contains a number of examples, in the top-level
``examples/`` directory. You must download the repository in order to run them:
they are not installed.

Running the examples
-------------------------

Run the programs in the ``examples/`` directory from that directory.
On \*nix, all the top-level modules of the examples are marked executable
and contain shebangs, so, for example, the following works::

    $ cd path/to/examples
    $ ./mproc.py

Of course, ``python ./mproc.py`` works too. On Windows, use::

    $ cd path\to\examples
    $ python ./mproc.py


Programs in the ``examples/`` directory
-----------------------------------------

This section catalogs the example programs by category and briefly
describes each one, sometimes in the imperative *a la* docstrings.

Simple examples
+++++++++++++++++++++

``root_logger.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Create a root logger with a stdout console handler at loglevel ``INFO``,
    and a file handler at default loglevel ``NOTSET``. Root loglevel is ``INFO``.

    :Logfile:  ``examples/_log/root_logger/logfile.log``

``child_logger_main.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Uses modules ``child_logger_sub_prop.py`` and ``child_logger_sub_noprop.py``.

    Create a non-root logger with two child loggers, one propagating and one not.
    The parent logger has a stderr handler and a file handler, shared by the
    propagating logger. The non-propagating logger creates its own stderr handler
    by cloning its parent's stderr handler; however, it uses the same file handler
    as its parent (and its sibling).

    Observe how the loglevels of the handlers and loggers determine what gets
    written to the two destinations.

    :Logfile:  ``examples/_log/child_loggers/child_loggers.log``


``child_logger2_main.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Uses ``child_logger2_sub_prop.py``, ``child_logger2_sub_noprop.py``.

    Give the root logger a stderr handler and a file handler. Create two loggers,
    one propagating and the other not. The non-propagating logger creates its own
    stderr handler by cloning the root's stderr handler; however, it uses the same
    file handler used by the root (and its sibling).

    Observe how the loglevels of the handlers and loggers determine what gets written
    to the two destinations.

    :Logfile:  ``examples/_log/child_loggers2/child_loggers2.log``

``dateformat.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A small example showing two uses of the ``dateformat`` parameter of
    ``add_formatter``.


Handler examples
+++++++++++++++++++

``use_library.py`` (use of a null handler)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A main program which configures logging, *and* uses a package (``library``)
    which *also* configures logging in its ``__init__`` module.
    The package sets up logging with a non-root logger at loglevel ``INFO``
    which uses a null handler; package methods log messages with that logger.
    The program adds a stdout handler to the root, with loglevel ``DEBUG``;
    the root loglevel is the default, ``WARNING``.

    The package's logger propagates, therefore messages logged by the package
    with loglevel at least ``INFO`` are written.


``SMTP_handler_just_one.py`` and ``SMTP_handler_two.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    These programs use ``add_email_handler`` to add SMTP handlers.
    ``SMTP_handler_just_one.py`` adds a single SMTP handler;
    ``SMTP_handler_two.py`` adds two, one with a filter, in order
    to send different email messages for different loglevels.

    .. attention::
        For these examples to work properly, you must edit
        ``examples/_smtp_credentials.py`` to contain a valid username,
        password and SMTP server.

``syslog.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    (*OS X aka macOS only*)
    Set the root logger level to ``DEBUG``, and add handlers:

        * add a stdout handler with loglevel ``WARNING``, and
        * use ``add_syslog_handler`` to add a syslog handler with default
          loglevel ``NOTSET``.

    Also see the example ``mproc_deco_syslog.py``, described :ref:`below <mproc_deco_syslog>`.

``queue_handler_listener.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    An example that illustrates how to use a QueueListener with `prelogging` so
    that messages can be logged on a separate thread. In this way, handlers that
    block and take long to complete (e.g. SMTP handlers, which send emails)
    won't make other threads (e.g. the UI thread) stall and stutter.

    For motivation, see `Dealing with handlers that block
    <https://docs.python.org/3/howto/logging-cookbook.html#dealing-with-handlers-that-block>`_
    in the `logging` Cookbook. We've adapted the code in that section to `prelogging`.

    Another approach can be found in the example ``mproc_approach__queue_handler_logging_thread.py``,
    described :ref:`below <mproc_two_approaches>`.

.. _mproc_examples:

Filter examples
++++++++++++++++++++++++++++++++

``filter-class-extra-static-data.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Passing extra static data to a class filter via keyword arguments to ``add_class_filter``
    to specify how different instances will filter messages.

    Described and walked through in the section on
    :ref:`providing extra, static data to a class filter <providing-extra-static-data-to-a-filter-class>`
    of the "Further Topics and Recipes" chapter.

``filter-callable-extra-static-data.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    The analogous construction – passing extra static data to a callable filter
    via keyword arguments to ``add_class_filter`` to specify how it will filter messages.

    Namedropped but not described in the section on
    :ref:`providing extra, static data to a callable filter <providing-extra-static-data-to-a-filter-class>`
    of "Further Topics and Recipes".

``filter-adding-fields--custom-formatter-keywords-for-fields.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This example illustrates adding custom fields and data to logged messages.
    It uses a custom formatter with two new keywords, ``user`` and ``ip``,
    and a class filter created with a callable data source – static initializing data
    for the filter, but a source of dynamic data.
    The filter's ``filter`` method adds attributes of the same names as the keywords
    to each ``LogRecord`` passed to it, calling the data source to obtain current
    values for these attributes.

    Loosely adapts the section
    `Using Filters to impart contextual information <https://docs.python.org/3/howto/logging-cookbook.html#using-filters-to-impart-contextual-information>`_
    of The Logging Cookbook.


Multiprocessing examples
++++++++++++++++++++++++++++++++

    Except for the ``mproc_approach_*.py`` examples, the programs described in
    this section all take command line arguments which tell them whether or not
    to use locking handlers.

    Usage for the programs that take command line parameters::

        ./program_name [--LOCKING | --NOLOCKING]
        ./program_name -h | --help

         Options (case-insensitive, initial letter suffices,
                  e.g. "--L" or "--n" or even -L):

         -L, --LOCKING      Use locking handlers       [default: True]
         -N, --NOLOCKING    Use non-locking handlers   [default: False]
         -h, --help         Write this help message and exit.

    When run without locking, the multiprocessing examples *will* eventually
    misbehave -- ``NUL`` (0) bytes will appear in the logged output, and messages
    logged by different processes will barge in on each other. The directory
    ``examples/_log saved`` contains subdirectories
    ``_log--2.7-runs``, ``_log--3.x-runs (I)`` and ``_log--3.x-runs (II)`` which
    capture several instances of this misbehavior. Though your mileage
    may vary, experience has shown that this expected misbehavior is more likely
    when these examples are run individually than when they're run via
    ``run_examples.py`` or ``run_all.py``.

    After running any of these examples, you can use ``check_for_NUL.py``
    to check whether or not its logfile output is garbled:

        ``$ ./check_for_NUL.py`` `filename`

    reports which if any lines of a text file `filename` contain ``NUL`` bytes.
    Here, `filename` would be the name of the logfile that the program wrote to.

``mproc.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A basic multiprocessing example that uses a non-propagating logger with
    a stdout handler and a file handler. The handlers are locking by default,
    non-locking if the ``-N`` command line flag is given.

    :Logfiles:  ``examples/_log/mproc/mproc_LOCKING.log``
                ``examples/_log/mproc/mproc_NONLOCKING.log``

``mproc2.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Another basic multiprocessing example that adds
    a stdout handler and a file handler to the root logger. The handlers are
    locking by default, optionally non-locking as explained above.

    :Logfiles:  ``examples/_log/mproc2/mproc2_LOCKING.log``
                ``examples/_log/mproc2/mproc2_NONLOCKING.log``

``mproc_deco.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Just like ``mproc2.py`` but using the `deco` package to set up multiprocessing.

    :Logfiles:  ``examples/_log/mproc_deco/logfile (LOCKING).log``
                ``examples/_log/mproc_deco/logfile (NONLOCKING).log``

``mproc_deco_rot_fh.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Adds a stdout handler and a rotating file handler to the root logger.
    The handlers are locking by default, optionally non-locking as explained above.
    This example uses `deco` to set up multiprocessing,

    :Logfiles:  ``examples/_log/mproc_deco_rot_fh/LOCKING/rot_fh.log``
                ``examples/_log/mproc_deco_rot_fh/LOCKING/rot_fh.log.1``
                ``...``
                ``examples/_log/mproc_deco_rot_fh/LOCKING/rot_fh.log.10``
                ``examples/_log/mproc_deco_rot_fh/NONLOCKING/rot_fh.log``
                ``examples/_log/mproc_deco_rot_fh/NONLOCKING/rot_fh.log.1``
                ``...``
                ``examples/_log/mproc_deco_rot_fh/NONLOCKING/rot_fh.log.10``

.. _mproc_deco_syslog:

``mproc_deco_syslog.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Adds a stdout handler and a syslog handler to the root logger.
    The handlers are locking by default, optionally non-locking as explained above.
    This example uses `deco` to set up multiprocessing,

.. _mproc_two_approaches:

``mproc_approach__locking_handlers.py`` and ``mproc_approach__queue_handler_logging_thread.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    These two programs illustrate two approaches to logging in the presence of
    multiprocessing: one uses `prelogging`\'s native locking handlers; the
    other uses a queue handler and a logging thread.

    See :ref:`mp-queue-and-logging-thread` in the chapter :ref:`further-topics-recipes`
    for (much) more about the latter.

    :locking handler logfiles:  ``examples/_log/mproc_LH/mplog.log``,
                                ``examples/_log/mproc_LH/mplog-errors.log``,
                                ``examples/_log/mproc_LH/mplog-foo.log``
    :queue handler logfiles:    ``examples/_log/mproc_QHLT/mplog.log``,
                                ``examples/_log/mproc_QHLT/mplog-errors.log``,
                                ``examples/_log/mproc_QHLT/mplog-foo.log``
