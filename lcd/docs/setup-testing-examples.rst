`lcd` Setup
===============

.. todo::
    Blahh blah blah

Requirements
---------------

The `lcd` package requires only Python 2.7 or 3.4+. It has no external
dependencies.

However, all examples (in the ``examples/`` subdirectory of the repository top
level) require `docopt`, and two examples require the `deco` package.

.. todo::
    Maybe change this: get rid of `docopt` dependency, use `argparse` instead.
    (Better just to use the standard library, yes?)
    Doing this only requires modifying one function:

        ``get_locking_pref(version='1') -> bool``

    in ``examples/_get_locking_pref.py``.


Installation
---------------

You can install `lcd` from PyPI (the Python Package Index) using ``pip``::

    $ pip install lcd

(Here and elsewhere, ``$`` at the beginning of a line indicates your command
prompt, whatever that may be.) Alternately, you can download a ``.zip`` or
``.tar.gz`` archive of the repository from github, uncompress it to a fresh
directory, and run::

    $ ./setup.py install

The latter approach lets you review the examples, which are not installed.
Whichever way you choose, ideally you'll do it in a virtual environment.


Running tests and examples
------------------------------

Tests are installed automatically, but examples are not.

The top level directory of the `lcd` repository (where ``setup.py`` also
resides) contains three executable scripts which run all tests, all examples,
or both: ``run_tests.py``, ``run_examples.py``, and ``run_all.py``.

Running tests
++++++++++++++

You can run all the tests before installing `lcd` by running the script
``run_tests.py`` in the top level directory of the repository::

    $ ./run_tests.py

Coverage from tests
~~~~~~~~~~~~~~~~~~~

`lcd` contains a very small amount of Python-2-only code, workarounds
for Py2 shortcomings.

+--------------------------------+--------+-------+
|| Module                        || Py 3  || Py 2 |
+================================+========+=======+
|| ``logging_config_dict.py``    || \99%  || 100% |
|| ``logging_config_dict_ex.py`` || \96%  || \98% |
|| ``locking_handlers.py``       || 100%  || 100% |
|| ``configurator.py``           || 100%  || 100% |
+--------------------------------+--------+-------+


Running examples
++++++++++++++++++

All examples require `docopt`, and two examples (``mproc_deco*.py``) require
the `deco` package. Examples are *not* installed; they're in the ``examples/``
subdirectory of the repository/archive.

You can run all the tests and examples before installing `lcd` by running the
script ``run_all.py`` in the repository directory:

    ``$ ./run_all.py``

When run without locking, the multiprocessing examples will eventually
misbehave -- NUL bytes will appear in the logged output, and messages logged by
different processes will barge in on each other. The subdirectories
``_log--2.7-runs``, ``_log--3.5-runs (I)`` and ``_log--3.5-runs (II)`` of
``examples/`` capture several instances of this misbehavior. Though your mileage
may vary, experience has shown that this expected misbehavior is more likely
when these examples are run individually, than when they're run via
``run_examples.py`` or ``run_all.py``.

Coverage from tests + examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Three lines of Python-2-only code prevent `lcd`  from having 100% coverage on
both language versions.

+--------------------------------+--------+-------+
|| Module                        || Py 3  || Py 2 |
+================================+========+=======+
|| ``logging_config_dict.py``    || \99%  || 100% |
|| ``logging_config_dict_ex.py`` || \97%  || 100% |
|| ``locking_handlers.py``       || 100%  || 100% |
|| ``configurator.py``           || 100%  || 100% |
+--------------------------------+--------+-------+
