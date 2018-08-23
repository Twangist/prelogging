.. _preset-formatters-chapter:

.. index:: formatter presets

Formatter Presets
--------------------------------------------------------

.. todo::
    FROM LCDict-features-and-usage (modify/condense)

    `prelogging` provides an extensible, modifiable collection of *formatter
    presets* — predefined formatter specifications which cover many needs.
    You can use the name of any of these presets as the ``formatter`` argument
    to ``add_*_handler`` methods and to ``set_handler_formatter``. `prelogging` ships
    with about a dozen of them, shown in :ref:`this table <preset-formatters-table>`.


.. _preset-formatters-table:

.. index:: formatter presets (shipped with prelogging — table)

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

.. todo::
    FROM LCDict-features-and-usage (modify/condense)

    Of course, the dozen or so formatter presets that `prelogging` contains,
    aren't a comprehensive collection, and probably won't meet everyone's needs
    or suit everyone's tastes. Therefore `prelogging` lets you add your own,
    and/or modify existing ones, using the ``update_formatter_presets_from_file(filename)``
    function. This function, and the format of the files it accepts, are described
    in the chapter :ref:`Formatter presets <preset-formatters-chapter>` following
    this one.

.. todo::
    Include a link (repeat it) to all the format-string keywords that `logging` recognizes
    Here it is:
    `the complete list of keywords that can appear in formatters <https://docs.python.org/3/library/logging.html#logrecord-attributes>`_.

.. _update_formatter_presets_from_file:

.. index:: update_formatter_presets_from_file function

The ``update_formatter_presets_from_file`` function
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. todo::
    Blah blah
