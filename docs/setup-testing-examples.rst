`logging_configuration` Setup
===========================

.. todo::
    Blahh blah blah ???

Requirements
---------------

The `logging_configuration` package requires only Python 3.4+ or 2.7. It has no external
dependencies.

Very little of `logging_configuration`\'s code varies between Python versions; however, to achieve
backwards compatibility with 2.7 we had to sacrifice, with great reluctance,
type annotations and keyword-only parameters. The `logging_configuration` package includes a copy
of the module ``six.py`` (version 1.10.0, for what it's worth), which it uses
sparingly (one decorator, one function, and one constant).

The `logging_configuration` distribution contains an ``examples/`` subdirectory. A few examples
(``mproc_deco*.py``) use the `deco <https://github.com/alex-sherman/deco>`_
package, which provides a "simplified parallel computing model for Python".
However, the examples are just for illustration (and code coverage), and aren't
installed with the `logging_configuration` package.

The distribution also contains subdirectories ``tests/`` and ``docs/``, which
similarly are not installed.

Installation
---------------

You can install `logging_configuration` from PyPI (the Python Package Index) using ``pip``::

    $ pip install logging_configuration

(Here and elsewhere, ``$`` at the beginning of a line indicates your command
prompt, whatever that may be.)

Alternately, you can download a ``.zip`` or ``.tar.gz`` archive of the
repository from github or PyPI, uncompress it to a fresh directory, ``cd`` to
that directory, and run::

    $ python setup.py install

On *nix systems, including macOS, ``setup.py`` is executable, so on those
platforms you can just run::

    $ ./setup.py install

Downloading and uncompressing the archive lets you review, run and/or copy the
tests and examples, which aren't installed by ``pip`` or ``setup.py``. Whichever
method you choose to install `logging_configuration`, ideally you'll do it in a virtual
environment.


Running tests and examples
------------------------------

The top-level directory of the `logging_configuration` distribution (where ``setup.py``
resides) has subdirectories ``tests/`` and ``examples/``, which contain just what
their names suggest. Neither of these sets of source files are installed.

In the top-level directory are three executable scripts — ``run_tests.py``,
``run_examples.py``, and ``run_all.py`` — which respectively run all tests, all
examples, or both.


Running tests
++++++++++++++

You can run all the tests before installing `logging_configuration` by running the script
``run_tests.py`` in the top level directory of the repository::

    $ ./run_tests.py


Alternately, you can run ::

    $ ./setup.py test

Coverage from tests
~~~~~~~~~~~~~~~~~~~

`logging_configuration` contains a small amount of Python-2-only code (workarounds
for Py2 shortcomings), and supports a few Python-3-only logging features.
In addition, several methods in ``logging_config_dict_ex.py`` add various
exotic handlers, which are easy to write examples for but difficult to test.

+----------------------------+--------+-------+
|| Module                    || Py 3  || Py 2 |
+============================+========+=======+
|| ``lcdictbasic.py``        || \99%  || \99% |
|| ``lcdict.py``             || \88%  || \88% |
|| ``locking_handlers.py``   || \89%  || \89% |
|| ``lcdict_builder_abc.py`` || 100%  || 100% |
+----------------------------+--------+-------+


Running examples
++++++++++++++++++

Examples are not installed; they're in the ``examples/`` subdirectory of the
distribution. You can run all the examples by running the script
``run_examples.py`` in the top-level directory:

    ``$ ./run_examples.py``

From the same directory, you can run all tests and examples with the script
``run_all.py``:

    ``$ ./run_all.py``

Two examples use the ``add_email_handler`` method to send emails. *In order to
run these without errors, you must first edit the file*
``examples/_smtp_credentials.py`` *to contain a valid username, password and
SMTP server.*

When run without locking, the multiprocessing examples *will* eventually
misbehave -- NUL bytes will appear in the logged output, and messages logged by
different processes will barge in on each other. The directory
``examples/_log saved`` contains subdirectories
``_log--2.7-runs``, ``_log--3.5-runs (I)`` and ``_log--3.5-runs (II)`` which
capture several instances of this misbehavior. Though your mileage
may vary, experience has shown that this expected misbehavior is more likely
when these examples are run individually than when they're run via
``run_examples.py`` or ``run_all.py``.

Coverage from tests + examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A few short passages, mostly Python-version-specific code, keep `logging_configuration` shy of
100% coverage when both tests and examples are run:

+----------------------------+--------+-------+
|| Module                    || Py 3  || Py 2 |
+============================+========+=======+
|| ``lcdictbasic.py``        || \99%  || 100% |
|| ``lcdict.py``             || \98%  || \96% |
|| ``locking_handlers.py``   || 100%  || 100% |
|| ``lcdict_builder_abc.py`` || 100%  || 100% |
+----------------------------+--------+-------+
