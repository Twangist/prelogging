from collections import namedtuple

__author__ = "Brian O'Neill"
__all__ = ('FormatterSpec', 'load_formatter_presets')

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


# TODO: Make these external -- some simple text file format?
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

def load_formatter_presets():
    # TODO: If/when formatter presets are external, load them here. Meanwhile:
    return __formatter_presets
