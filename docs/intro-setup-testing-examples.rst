Introduction and Setup
============================================

`prelogging` is a package for setting up, or *configuring*, the
logging facility of the Python standard library. To *configure logging* is to
specify the logging entities you wish to create — formatters, handlers, optional
filters, and loggers — as well as which of them use which others.

Once configured, logging messages with the `logging` facility is simple and
powerful; configuration presents the only challenge. `logging` provides a couple
of approaches to configuration — static, using a dict or an analogous YAML text
file; and dynamic, using the `logging` API — both of which have their shortcomings.

`prelogging` offers a hybrid approach: a streamlined, consistent API for
incrementally constructing a dict used to configure logging statically.
As you build the configuration dict, by default `prelogging` checks for possible
mistakes and issues warnings on encountering them. `prelogging` also supplies
missing functionality: it provides multiprocessing-safe logging to the console,
to files and rotating files, and to `syslog`.


Requirements
---------------

The `prelogging` package requires only Python 3.4+ or 2.7. It has no external
dependencies.

Very little of `prelogging`\'s code is sensitive to Python 3 vs 2.
To achieve backwards compatibility with 2.7 we sacrificed, with some
reluctance, type annotations and keyword-only parameters. To address the
few remaining differences, we've used `six` sparingly (one decorator, one
function, and one constant). The `prelogging` package includes a copy of the ``six.py``
module (v1.10.0, for what it's worth), so no separate installation is required.

The `prelogging` distribution contains an ``examples/`` subdirectory. A few
examples (``mproc_deco*.py``) use the `deco <https://github.com/alex-sherman/deco>`_
package, which provides a "simplified parallel computing model for Python".
However, the examples are just for illustration (and code coverage), and aren't
installed with the `prelogging` package.

The distribution also contains subdirectories ``tests/`` and ``docs/``, which
similarly are not installed.

Installation
---------------

You can install `prelogging` from PyPI (the Python Package Index) using ``pip``::

    $ pip install prelogging

(Here and elsewhere, ``$`` at the beginning of a line indicates your command
prompt, whatever that may be.)

Alternately, you can

* clone the github repo, or
* download a ``.zip`` or ``.tar.gz`` archive of the repository
  from github or PyPI, uncompress it to a fresh directory, change to
  that directory, and run the command::

    $ python setup.py install

On \*nix systems, including macOS, ``setup.py`` is executable and has a proper
`shebang <https://en.wikipedia.org/wiki/Shebang_(Unix)>`_, so on those
platforms you can just say::

    $ ./setup.py install

Downloading and uncompressing the archive lets you review, run and/or copy the
tests and examples, which aren't installed by ``pip`` or ``setup.py``. Whichever
method you choose to install `prelogging`, ideally you'll do it in a `virtual
environment <https://docs.python.org/3/tutorial/venv.html?highlight=virtual>`_.


Running tests and examples
------------------------------

The top-level directory of the `prelogging` distribution (where ``setup.py``
resides) has subdirectories ``tests/`` and ``examples/``, which contain just
what their names suggest.

In the top-level directory are three scripts — ``run_tests.py``,
``run_examples.py``, and ``run_all.py``, all executable on \*nix platforms —
which respectively run all tests, all examples, or both.


Running tests
++++++++++++++

You can run all the tests before installing `prelogging` by running the script
``run_tests.py`` in the top level directory of the repository::

    $ python run_tests.py


Alternately, you can run ::

    $ python setup.py test


Coverage from tests
~~~~~~~~~~~~~~~~~~~

`prelogging` contains a small amount of Python-2-only code (workarounds
for Py2 shortcomings), and supports a few Python-3-only logging features.
In addition, several methods in ``lcdict.py`` add various exotic handlers,
which are easy to write examples for but difficult to test (coverage for this
module increases to 98%/96% when examples are included — see the following section).

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

    ``$ python run_examples.py``

From the same directory, you can run all tests and examples with the script
``run_all.py``:

    ``$ python run_all.py``

Note: the examples that use ``deco`` of course require that package to be installed;
the SMTP examples require that you edit ``examples/_smtp_credentials.py`` to contain
valid email credentials.

The section :ref:`guide-to-examples` catalogs all the examples and briefly
describes each one.

Coverage from tests + examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A few short passages, mostly Python-major-version-specific code, keep `prelogging`
shy of 100% coverage when both tests and examples are run:

+----------------------------+--------+-------+
|| Module                    || Py 3  || Py 2 |
+============================+========+=======+
|| ``lcdictbasic.py``        || \99%  || 100% |
|| ``lcdict.py``             || \98%  || \96% |
|| ``locking_handlers.py``   || 100%  || 100% |
|| ``lcdict_builder_abc.py`` || 100%  || 100% |
|| ``formatter_presets.py``  || 100%  || 100% |
+----------------------------+--------+-------+
