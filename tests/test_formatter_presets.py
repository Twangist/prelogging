__author__ = 'brianoneill'

from prelogging.formatter_presets import (
    FormatterSpec, _formatter_presets, _make_formatter_specs, update_formatter_presets_from_file
)
from unittest import TestCase

import sys
import io
from prelogging.six import PY2

# ---------------------------------------------------------------------------
# update_formatter_presets_from_file(lines)
# ---------------------------------------------------------------------------
if PY2: FileNotFoundError = IOError


class Test_update_formatter_presets(TestCase):

    def test_LCDict_startup(self):
        import prelogging.lcdict
        d = {
            'msg': FormatterSpec("%(message)s"),
            'level_msg': FormatterSpec('%(levelname)-8s: %(message)s'),
            'process_msg': FormatterSpec('%(processName)-10s: %(message)s'),
            'logger_process_msg': FormatterSpec('%(name)-20s: %(processName)-10s: %(message)s'),
            'logger_level_msg': FormatterSpec('%(name)-20s: %(levelname)-8s: %(message)s'),
            'logger_msg': FormatterSpec('%(name)-20s: %(message)s'),
            'process_level_msg': FormatterSpec('%(processName)-10s: %(levelname)-8s: %(message)s'),
            'process_time_level_msg': FormatterSpec('%(processName)-10s: %(asctime)s: %(levelname)-8s: %(message)s'),
            'process_logger_level_msg': FormatterSpec('%(processName)-10s: %(name)-20s: %(levelname)-8s: %(message)s'),
            'process_time_logger_level_msg': FormatterSpec('%(processName)-10s: %(asctime)s:'
                                                           ' %(name)-20s: %(levelname)-8s: %(message)s'),
            'time_logger_level_msg': FormatterSpec('%(asctime)s: %(name)-20s: %(levelname)-8s: %(message)s'),
        }
        self.assertEqual(d, _formatter_presets)

    def test_FileNotFound(self):
        # Swap stderr first
        _stderr = sys.stderr
        sio_err = io.StringIO()
        sys.stderr = sio_err

        update_formatter_presets_from_file('/nosuchfile_98765432.txt')

        self.assertEqual(
            sio_err.getvalue(),
            "File '/nosuchfile_98765432.txt' not found\n"
        )
        # unswap stderr, unnecessarily
        sys.stderr = _stderr

    def test_LCDict_BadStartup(self):

        # Swap stderr first
        _stderr = sys.stderr
        sio_err = io.StringIO()
        sys.stderr = sio_err

        # write to stderr:
        # "File formatter_presets_badfile.txt, line 2: expected key:value"
        update_formatter_presets_from_file('formatter_presets_badfile.txt')

        self.assertEqual(
            sio_err.getvalue(),
            "File formatter_presets_badfile.txt, line 2: expected key:value\n"
        )
        # unswap stderr, unnecessarily
        sys.stderr = _stderr


# ---------------------------------------------------------------------------
# _make_formatter_specs(lines)
# ---------------------------------------------------------------------------
# TODO -- TESTS
"""
Mostly, test _make_formatter_specs(lines)

-- 8 errors to test (search: "# | raise")
-- empty file
-- only blank lines file


To test _read_...(lines),
you can generate lines from a (multiline) string mls by doing
    lines = mls.splitlines(True)
where the arg is `keepends`: True means keep trailing '\n'
"""


class Test_read_formatter_presets(TestCase):

    def test_MissingFormatKey(self):
        s = '''\
somename

'''
        with self.assertRaises(ValueError) as exc:
            _make_formatter_specs(s.splitlines(True))

        self.assertEqual(str(exc.exception),
                         "line 2: 'format' key:value missing in 'somename'")

    def test_ExpectingNameGotIndentedLine(self):
        s1 = '''\

    something
'''
        s2 = '''\
somethingElse
    format: some_format_str

    indented
'''
        with self.assertRaises(ValueError) as exc1:
            _make_formatter_specs(s1.splitlines(True))
        self.assertEqual(str(exc1.exception),
                         "line 2: expected name, starting in column 1")

        with self.assertRaises(ValueError) as exc2:
            _make_formatter_specs(s2.splitlines(True))
        self.assertEqual(str(exc2.exception),
                         "line 4: expected name, starting in column 1")

    def test_BadKeyValue(self):
        s1 = '''\
name
    : xyz
'''
        s2 = '''\
name
    abc:
'''
        s3 = '''\
name
    style: '%
    abc
'''
        with self.assertRaises(ValueError) as exc1:
            _make_formatter_specs(s1.splitlines(True))
        self.assertEqual(str(exc1.exception),
                         "line 2: key must be nonempty")

        with self.assertRaises(ValueError) as exc2:
            _make_formatter_specs(s2.splitlines(True))
        self.assertEqual(str(exc2.exception),
                         "line 2: value must be nonempty")

        with self.assertRaises(ValueError) as exc3:
            _make_formatter_specs(s3.splitlines(True))
        self.assertEqual(str(exc3.exception),
                         "line 3: expected key:value")

    def test_NoFormatKey(self):
        s = '''\
somename
    style: '%
'''
        with self.assertRaises(ValueError) as exc:
            _make_formatter_specs(s.splitlines(True))
        self.assertEqual(str(exc.exception),
                         "line 2: 'format' key:value missing in 'somename'")

        s2 = '''\
somename
    style: '%

'''
        with self.assertRaises(ValueError) as exc2:
            _make_formatter_specs(s2.splitlines(True))
        self.assertEqual(str(exc2.exception),
                         "line 3: 'format' key:value missing in 'somename'")

    def test_BadKey(self):
        s = '''\
somename
    style: '%
    badbadkey: val
'''
        with self.assertRaises(ValueError) as exc:
            _make_formatter_specs(s.splitlines(True))
        self.assertEqual(str(exc.exception),
                         "line 3: bad key 'badbadkey' -- must be one of "
                         "'format', 'dateformat', 'style'")

