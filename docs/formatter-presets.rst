.. _preset-formatters-chapter:

.. index:: formatter presets

Formatter Presets
--------------------------------------------------------

`prelogging` provides an extensible, modifiable collection of *formatter
presets* — predefined formatter specifications which you can reference by
name as the ``formatter`` argument to ``add_*_handler`` and
``set_handler_formatter`` methods of ``LCDict``, without having to first
call ``add_formatter``. We've already seen them in use, in the
:ref:`first example of using prelogging <config-use-case-lcdict>`
and in the previous chapter's section on
:ref:`using formatter presets <formatter_presets_in_LCDict>`.

When first loaded, `prelogging` provides these presets:

.. index:: formatter presets (shipped with prelogging — table)
.. _preset-formatters-table:

+--------------------------------------+-----------------------------------------------------------------------------------+
|| Formatter name                      || Format string                                                                    |
+======================================+===================================================================================+
|| ``'msg'``                           || ``'%(message)s'``                                                                |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'level_msg'``                     || ``'%(levelname)-8s: %(message)s'``                                               |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'process_msg'``                   || ``'%(processName)-10s: %(message)s'``                                            |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'logger_process_msg'``            || ``'%(name)-20s: %(processName)-10s: %(message)s'``                               |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'logger_level_msg'``              || ``'%(name)-20s: %(levelname)-8s: %(message)s'``                                  |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'logger_msg'``                    || ``'%(name)-20s: %(message)s'``                                                   |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'process_level_msg'``             || ``'%(processName)-10s: %(levelname)-8s: %(message)s'``                           |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'process_time_level_msg'``        || ``'%(processName)-10s: %(asctime)s: %(levelname)-8s: %(message)s'``              |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'process_logger_level_msg'``      || ``'%(processName)-10s: %(name)-20s: %(levelname)-8s: %(message)s'``              |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'process_time_logger_level_msg'`` || ``'%(processName)-10s: %(asctime)s: %(name)-20s: %(levelname)-8s: %(message)s'`` |
+--------------------------------------+-----------------------------------------------------------------------------------+
|| ``'time_logger_level_msg'``         || ``'%(asctime)s: %(name)-20s: %(levelname)-8s: %(message)s'``                     |
+--------------------------------------+-----------------------------------------------------------------------------------+


This collection is by no means comprehensive, nor could it be. (`logging` recognizes
about 20 `keywords in format strings <https://docs.python.org/3/library/logging.html#logrecord-attributes>`_;
you can even use your own keywords, as shown in
:ref:`adding-custom-fields-and-data-to-messages-with-formatter-and-filter`;
these can all be combined in infinitely many format strings.)
The names of these presets probably won't be to everyone's liking either (``level`` not ``levelname``;
``msg`` and ``process``, which are themselves recognized keywords, rather than ``message``
and ``processName``).
Nevertheless, formatter presets are a useful facility, especially across multiple projects.
Therefore, `prelogging` lets you add your own formatter presets, and/or modify existing ones.
Two functions make that possible:

    * ``update_formatter_presets(multiline_str)`` reads descriptions of formatters in
      a multiline string;
    * ``update_formatter_presets_from_file(filename)`` reads descriptions of formatters
      from a text file;

Both functions update the collection of formatter presets.

**Note**: The changes and additions made by these functions do **not** persist
after your program exits.

Generally, you call one of these functions, once, after importing `prelogging`
or things from it, and before creating an ``LCDict`` and populating it using your new
or improved formatter presets.

The following subsections describe these functions and the expected formats of
their arguments. It's convenient to present the file-based function first.

------------------------------------------------------------------------------

.. index:: update_formatter_presets_from_file function
.. _update_formatter_presets_from_file:

The ``update_formatter_presets_from_file`` function
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. autofunction:: prelogging.formatter_presets.update_formatter_presets_from_file

This function basically passes the contents of the file to ``update_formatter_presets``,
described below.

File format
~~~~~~~~~~~~

This functions expects a text file consisting of:

    * zero or more blank lines, followed by
    * zero or *formatter descriptions*, all separated by one or more blank lines.

A blank line consists only of whitespace. A *formatter description* is a group of
lines consisting of a `name`, beginning in column 1 on a line by itself, followed
by one or more indented lines each containing a `key` ``:`` `value` pair, and all
subject to the following conditions:

    * Each `key` must be one of ``format``, ``dateformat``, ``style``.
      ``format`` is required; the others are optional.
    * If a `value` contains spaces then it should be enclosed in quotes (single or double);
      otherwise, enclosing quotes are optional (any outermost matching quotes are removed).
    * A `name` can contain spaces, and does not have to be quoted unless you want it to have
      initial or trailing whitespace.
    * In a `key` ``:`` `value` pair, zero or more spaces may precede and follow the colon.
    * The `value` given for ``style`` should be one of ``%`` ``{`` ``$``; if ``style`` is omitted
      then it defaults to ``%``. (Under Python 2, only ``%`` is allowed, so if you're still using
      that then you should omit ``style``.)

These keys and values are as in the :ref:`LCDictBasic.add_formatter <LCDB_add_formatter-docstring>`
method.

Example 1 – basic and corner cases
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Here's an example of a valid/well-formed file (assume the names begin in column 1)::

    name_level_message
        format: '%(name)s - %(levelname)s - %(message)s'

    name level message
        format: '%(name)s - %(levelname)s - %(message)s'

    datetime_name_level_message
        format    : '{asctime}: {name:15s} - {levelname:8s} - {message}'
        dateformat: '%Y.%m.%d %I:%M:%S %p'
        style: {

    '    his formatter    '
        format:%(message)s

If the file passed to ``update_formatter_presets_from_file`` has ill-formed contents,
the function writes an appropriate error message to ``stderr``, citing the file name
and offending line number, and the collection of formatter presets remains unchanged.

.. index:: formatter presets (formatter_presets.txt – declares default collection)

Example 2 – ``formatter_presets.txt`` declares `prelogging`'s formatter presets
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Another example of a valid file containing formatter presets is the text file
``formatter_presets.txt`` in the `prelogging` directory. `prelogging` creates
its stock of formatter presets by calling

    ``update_formatter_presets_from_file(``\ *path/to/* ``'formatter_presets.txt')``

when the ``lcdict`` module is loaded.

.. index:: update_formatter_presets function
.. _update_formatter_presets:

------------------------------------------------------------------------------

The ``update_formatter_presets`` function
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. autofunction:: prelogging.formatter_presets.update_formatter_presets

For example, all of these are equivalent well-formed possible arguments::

        # <-- assume that's column 1

            s1 = '''\
        myformatter
            format: '%(message)s'
            style: '%'
        '''
            s2 = '''\
            myformatter
                format: '%(message)s'
                    style: '%'
            '''
            s2 = '''\
                myformatter
                  format: '%(message)s'
                  style: '%'
            '''

Note that each triple-quote beginning a multiline string is followed by ``\``,
so that the logical line `n` is not actually line `n`\+1.

If the string passed to ``update_formatter_presets`` is ill-formed, the function
writes an appropriate error message to ``stderr``, citing the offending line
number, and the collection of formatter presets remains unchanged.
