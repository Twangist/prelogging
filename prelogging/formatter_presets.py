from collections import namedtuple
import sys

__author__ = "Brian O'Neill"
__all__ = ('update_formatter_presets', 'FormatterSpec')

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
# update_formatter_presets
# -----------------------------------------------------------------------

def update_formatter_presets(filename):       # -> Dict[str, FormatterSpec]
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        #  | raise
        # print("File '%s' not found" % filename, file=sys.stderr)
        # Py2
        sys.stderr.write("File '%s' not found\n" % filename)
        return

    try:
       new_formatter_specs = _read_formatter_presets(lines)
    except ValueError as e:
        #  | raised, bubbled up
        # print(..., file=sys.stderr)
        # Py2
        sys.stderr.write(("File %s, " % filename) + str(e) + "\n")
        return

    _formatter_presets.update(new_formatter_specs)


# -----------------------------------------------------------------------
# (helpers)
# -----------------------------------------------------------------------

# Line types
NAME = 0
KEY_VAL = 1
BLANK = 2


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
        raise ValueError("expected key:value")                  # | raise

    return KEY_VAL, (_clean(parts[0], "key"), _clean(parts[1], "value"))


def _read_formatter_presets(lines):
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
            # TODO: Simplify. Regrettably, this got convoluted. Without "try"
            #  |    and `bad_key_value`, error message would be "bad key:value"
            #  |    rather than "expected name", when `expecting == NAME` and
            #  |    an indented line is encountered.
            bad_key_value = False
            try:
                linetype, data = _parse_line(line)
            except ValueError as valerr:
                bad_key_value = True

            if expecting == NAME:
                try:
                    linetype, data = _parse_line(line)
                except ValueError as valerr:
                    bad_key_value = True

                if linetype == NAME:
                    name = data
                    fields = {'style': '%'}
                    expecting = KEY_VAL
                elif bad_key_value:
                    raise ValueError("expected name, starting in column 1") # | raise
                elif linetype == BLANK:
                    continue

            elif bad_key_value:
                raise valerr

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
                else:   # linetype == NAME
                    raise ValueError("expected key:value")              # | raise

        except ValueError as e:
            raise ValueError(("line %d: " % (lineno+1)) + str(e))

    if fields:
        add_new_fs()
    return new_formatter_specs


if __name__ == '__main__':
    # path to this module: __file__
    # call update_formatter_presets on path + 'formatter_presets.txt'
    import os
    formatter_presets_filename = os.path.join(
                                    os.path.dirname(__file__),
                                    'formatter_presets.txt')
    update_formatter_presets(formatter_presets_filename)

    # compare formatter_presets_ with this:
    __formatter_presets = {
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
    print("Results OK:", _formatter_presets == __formatter_presets)
