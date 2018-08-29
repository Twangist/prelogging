from collections import namedtuple
import sys
from textwrap import dedent
from .six import PY2

__author__ = "Brian O'Neill"
__all__ = ['update_formatter_presets_from_file', 'update_formatter_presets']

# -----------------------------------------------------------------------
# FormatterSpec -- namedtuple subclass for static declaration
#                  of formatter specifications
# -----------------------------------------------------------------------

_formatter_spec_fields = ('format', 'dateformat', 'style')


class FormatterSpec( namedtuple('_FormatterSpec_', _formatter_spec_fields) ):
    """A namedtuple-derived lightweight class representing formatters.
    We subclass in order to allow variant spellings for parameters,
    to allow default values, and to easily convert to a dict.
    """
    __slots__ = ()

    def __new__(cls, format,
                datefmt=None,
                dateformat=None,
                style='%'):
        """
        :param format: a (logging) format string
        :param datefmt: a date-format string; mutually exclusive with dateformat
        :param dateformat: a date-format string; mutually exclusive with datefmt
        :param style: one of "%{$"
        """
        dateformat = datefmt or dateformat
        return super(FormatterSpec, cls).__new__(cls, format, dateformat, style)

    def to_dict(self):
        """
        Return a dict representation, whose keys are ``_formatter_spec_fields``
        except that 'dateformat' is changed to 'datefmt'),
        and which omits items with ``None`` values.

        :return: a dict
        """
        d = {k: getattr(self, k) for k in _formatter_spec_fields}
        d['datefmt'] = d.pop('dateformat', None)
        return {k: v for k, v in d.items() if v}


_formatter_presets = {}      # type: Dict[str, FormatterSpec]


# -----------------------------------------------------------------------
# update_formatter_presets_from_file
# -----------------------------------------------------------------------
if PY2: FileNotFoundError = IOError


def update_formatter_presets_from_file(filename):
    """
    .. _update_formatter_presets_from_file-docstring:

    Create a dict of "formatter specifications" from the contents of the file,
    and update the internal collection of formatter presets with that.

    :param str filename: a filename
    """
    try:
        with open(filename, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        #  | raise
        # print("File '%s' not found" % filename, file=sys.stderr)
        # Py2 horror
        s = "File '%s' not found\n" % filename
        if PY2: s = unicode(s)
        sys.stderr.write(s)
        return

    _update_formatter_presets(text, _errmsg_prefix="File %s, " % filename)


def _update_formatter_presets(multiline_str, _errmsg_prefix=''):
    """
    See ``update_formatter_presets``.

    :param _errmsg_prefix: as for ``update_formatter_presets``.
    :param _errmsg_prefix: (str) Internal arg, used by ``update_formatter_presets_from_file``.
        Any message will be prefixed with this.
    """
    # splitlines arg is `keepends` i.e. trailing '\n's. Omission: because PY2.
    lines = dedent(multiline_str).splitlines(True)
    try:
        new_formatter_specs = _make_formatter_specs(lines)
    except ValueError as e:
        #  | raised, bubbled up
        # print(..., file=sys.stderr)
        # Py2 horror
        s = _errmsg_prefix + str(e) + "\n"
        if PY2: s = unicode(s)
        sys.stderr.write(s)
        return

    _formatter_presets.update(new_formatter_specs)


def update_formatter_presets(multiline_str):
    """
    .. _update_formatter_presets-docstring:

    Create a dict of "formatter specifications" from ``multiline_str``, and update
    the internal collection of formatter presets with that.

    :param multiline_str: A multiline string which, when ``dedent``\ed,
        conforms to the format of files expected by ``update_formatter_presets_from_file``.
        This function calls ``dedent`` on ``multiline_str``, so that you don't have to.
        (See `dedent <https://docs.python.org/3/library/textwrap.html#textwrap.dedent>`_.)
        That is, names in the file don't have to begin in column 1; they can begin
        in any column, as long as they all begin in the *same* column, and as long
        as key:value lines are indented even more.
    """
    _update_formatter_presets(multiline_str)

# -----------------------------------------------------------------------
# (helpers)
# -----------------------------------------------------------------------

# Line types
NAME = 0
KEY_VAL = 1
BAD_KEY_VAL = 2
BLANK = 3


def _clean(s, part_type):           # -> str
    """strip, unquote s"""
    s = s.strip()
    if not s:
        raise ValueError("%s must be nonempty" % part_type)     # | raise
    if len(s) > 1 and s[0] == s[-1] and s[0] in ('"', "'"):
        s = s[1: -1]
    return s


def _parse_line(line):   # -> Tuple[LineType, (str or Tuple[str, str] or None)]
    stripped = line.strip()
    if not stripped:
        return BLANK, None
    if not line[0].isspace():
        # Note, ':' allowed in names; spaces allowed in names if they're
        #  .    quoted; any outermost quotes are removed.
        return NAME, _clean(stripped, "name")
    # it's a key/value pair or bust
    parts = stripped.split(':', 1)          # PY2, no kwd arg (maxsplit=1)
    if len(parts) != 2:
        return BAD_KEY_VAL, (parts)
    return KEY_VAL, (_clean(parts[0], "key"), _clean(parts[1], "value"))


def _make_formatter_specs(lines):             # -> Dict[str, FormatterSpec]
    keys = ('format', 'dateformat', 'style')

    name = ''
    new_formatter_specs = {}
    expecting = NAME
    fields = {}

    def add_new_fs():
        # Commented out because PY2
        # nonlocal new_formatter_specs, name  # not needed; just for clarity

        if 'format' not in fields:
            raise ValueError("'format' key:value missing in '%s'" % name)    # | raise
        fmt = fields.pop('format')
        new_formatter_specs[name] = FormatterSpec(fmt, **fields)

    # Run state machine
    for lineno, line in enumerate(lines):
        try:
            linetype, data = _parse_line(line)

            if expecting == NAME:
                if linetype == NAME:
                    name = data
                    fields = {'style': '%'}
                    expecting = KEY_VAL
                elif linetype == BLANK:
                    continue
                elif linetype in (KEY_VAL, BAD_KEY_VAL):
                    raise ValueError("expected name, starting in column 1") # | raise

            elif expecting == KEY_VAL:
                if linetype == KEY_VAL:
                    key, value = data
                    if key not in keys:
                        raise ValueError("bad key '%s' -- must be one of "
                                         "'format', 'dateformat', 'style'" % key)          # | raise
                    fields[key] = value
                    # expecting = KEY_VAL
                elif linetype == BLANK:
                    add_new_fs()
                    fields = {}
                    expecting = NAME
                else:                   # linetype in (NAME, BAD_KEY_VAL)
                    raise ValueError("expected key:value")              # | raise

        except ValueError as e:
            raise ValueError(("line %d: " % (lineno+1)) + str(e))

    if fields:
        try:
            add_new_fs()            # raises, if 'format' key missing
        except ValueError as e:
            raise ValueError(("line %d: " % (lineno+1)) + str(e))

    return new_formatter_specs
