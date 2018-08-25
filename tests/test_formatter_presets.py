__author__ = 'brianoneill'

from prelogging.formatter_presets import (
    FormatterSpec, _formatter_presets, _make_formatter_specs,
    update_formatter_presets_from_file, update_formatter_presets
)
from unittest import TestCase
from textwrap import dedent
import sys
import io
from prelogging.six import PY2
import logging

# TODO? maybe low priority
# These are, largely, negative tests. Almost all of them test that
# things that should # fail, do fail, in the expected ways. Nearly none
# confirm success with expected results.

# ---------------------------------------------------------------------------
# update_formatter_presets_from_file(lines)
# ---------------------------------------------------------------------------
if PY2: FileNotFoundError = IOError


class Test_update_formatter_presets_from_file(TestCase):

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
        # _formatter_presets contains d:
        for k in d:
            self.assertIn(k, _formatter_presets)
            self.assertEqual(d[k], _formatter_presets[k])

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

        # Swap stderr
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


class Test_update_formatter_presets(TestCase):
    def test_update_formatter_presets_exception(self):

        # Swap stderr first
        _stderr = sys.stderr
        sio_err = io.StringIO()
        sys.stderr = sio_err

        s = """\
        myformatter:
            format: '{asctime}: {name}: {levelname}: {message}'
            style: '{'
                : valOfNoKey
        """
        # write to stderr:
        update_formatter_presets(s)

        self.assertEqual(sio_err.getvalue(),
                         "line 4: key must be nonempty\n")
        # unswap stderr, unnecessarily
        sys.stderr = _stderr

# ---------------------------------------------------------------------------
# _make_formatter_specs(lines)
# ---------------------------------------------------------------------------

class Test_read_formatter_presets(TestCase):

    def test_MissingFormatKey(self):
        s = '''\
        somename

        '''
        with self.assertRaises(ValueError) as exc:
            _make_formatter_specs(dedent(s).splitlines(True))

        self.assertEqual(str(exc.exception),
                         "line 2: 'format' key:value missing in 'somename'")

    def test_ExpectingNameGotIndentedLine(self):
        s1 = '''\

            something

        something-else
        '''
        s2 = '''\
        another-thing
            format: some_format_str

            indented
        '''
        with self.assertRaises(ValueError) as exc1:
            _make_formatter_specs(dedent(s1).splitlines(True))
        self.assertEqual(str(exc1.exception),
                         "line 2: expected name, starting in column 1")

        with self.assertRaises(ValueError) as exc2:
            _make_formatter_specs(dedent(s2).splitlines(True))
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
            style: %
            abc
        '''
        with self.assertRaises(ValueError) as exc1:
            _make_formatter_specs(dedent(s1).splitlines(True))
        self.assertEqual(str(exc1.exception),
                         "line 2: key must be nonempty")

        with self.assertRaises(ValueError) as exc2:
            _make_formatter_specs(dedent(s2).splitlines(True))
        self.assertEqual(str(exc2.exception),
                         "line 2: value must be nonempty")

        with self.assertRaises(ValueError) as exc3:
            _make_formatter_specs(dedent(s3).splitlines(True))
        self.assertEqual(str(exc3.exception),
                         "line 3: expected key:value")

    def test_NoFormatKey(self):
        s = '''\
        somename
            style: %
        '''
        with self.assertRaises(ValueError) as exc:
            _make_formatter_specs(dedent(s).splitlines(True))
        self.assertEqual(str(exc.exception),
                         "line 2: 'format' key:value missing in 'somename'")

        s2 = '''\
        somename
            style: {

        '''
        with self.assertRaises(ValueError) as exc2:
            _make_formatter_specs(dedent(s2).splitlines(True))
        self.assertEqual(str(exc2.exception),
                         "line 3: 'format' key:value missing in 'somename'")

    def test_BadKey(self):
        s = '''\
        somename
            style: '%'
            badbadkey: val
        '''
        with self.assertRaises(ValueError) as exc:
            _make_formatter_specs(dedent(s).splitlines(True))
        self.assertEqual(str(exc.exception),
                         "line 3: bad key 'badbadkey' -- must be one of "
                         "'format', 'dateformat', 'style'")


class TestStyle(TestCase):

    def test_style_quotes(self):
        from prelogging import LCDict
        s = '''\
        myformatter
            format: '** %(name)s - %(levelname)s - %(message)s'
            style: '%'
        '''
        update_formatter_presets(s)

        # Swap stderr
        _stderr = sys.stderr
        sio_out = io.StringIO()
        sys.stderr = sio_out

        lcd = LCDict(attach_handlers_to_root=True)
        lcd.add_stderr_handler('con', formatter='myformatter')
        lcd.config()

        import logging
        root = logging.getLogger()
        root.warning(u'Yo, muh man')        # PY2: 'u' prefix

        self.assertEqual(sio_out.getvalue(),
                         "** root - WARNING - Yo, muh man\n")
        # unswap stderr, unnecessarily
        sys.stderr = _stderr

    def test_style_no_quotes(self):
        from prelogging import LCDict
        s = '''\
        myformatter
            format: '__%(message)s__'
            style: %
        '''
        update_formatter_presets(s)

        # Swap stderr
        _stderr = sys.stderr
        sio_out = io.StringIO()
        sys.stderr = sio_out

        lcd = LCDict(attach_handlers_to_root=True)
        lcd.add_stderr_handler('con', formatter='myformatter')
        lcd.config()
        root = logging.getLogger()
        root.warning(u'Yo, muh man')        # PY2: 'u' prefix

        self.assertEqual(sio_out.getvalue(),
                         "__Yo, muh man__\n")
        # unswap stderr, unnecessarily
        sys.stderr = _stderr


class TestSpacesInName(TestCase):

    def test_internal_space(self):
        from prelogging import LCDict
        s = '''\
        my formatter
            format: '%(name)s - %(levelname)s - %(message)s'
            style: %
        '''
        update_formatter_presets(s)

        # Swap stderr
        _stderr = sys.stderr
        sio_out = io.StringIO()
        sys.stderr = sio_out

        lcd = LCDict(attach_handlers_to_root=True)
        lcd.add_stderr_handler('con', formatter='my formatter')
        lcd.config()

        import logging
        root = logging.getLogger()
        root.warning(u'Hello')        # PY2: 'u' prefix

        self.assertEqual(sio_out.getvalue(),
                         "root - WARNING - Hello\n")
        # unswap stderr, unnecessarily
        sys.stderr = _stderr

    def test_init_trailing_space(self):
        from prelogging import LCDict
        s = '''\
        ' my formatter '
            format: '%(name)s - %(levelname)s - %(message)s'
            style: %
        '''
        update_formatter_presets(s)

        # Swap stderr
        _stderr = sys.stderr
        sio_out = io.StringIO()
        sys.stderr = sio_out

        lcd = LCDict(attach_handlers_to_root=True)
        lcd.add_stderr_handler('con', formatter=' my formatter ')
        lcd.config()

        import logging
        root = logging.getLogger()
        root.warning(u'Hello')        # PY2: 'u' prefix

        self.assertEqual(sio_out.getvalue(),
                         "root - WARNING - Hello\n")
        # unswap stderr, unnecessarily
        sys.stderr = _stderr
