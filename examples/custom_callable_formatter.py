from prelogging import LCDict
import logging

KEYWORD = 'my_keyword'

# "callable formatter"
def callable_formatter(logrecord, format, **kwds):
    return (
        ("callable_formatter [ %r: %r]: " % (KEYWORD, kwds.get(KEYWORD, None)))
        +
        (format % vars(logrecord))
    )


def formatter_factory(**kwargs):
    format = kwargs.pop('format')
    formatter = lambda record: callable_formatter(record, format, **kwargs)
    formatter.format = formatter  # `logging` requires this
    return formatter


if __name__ == '__main__':
    lcd = LCDict(attach_handlers_to_root=True)
    lcd.add_formatter( 'my_formatter',
                       format='%(name)s - %(levelname)s - %(msg)s',
                       # dateformat=...,
                       # style='%',
                       ** {'()': formatter_factory,
                          KEYWORD: 'my_value'} )
    lcd.add_stdout_handler('out', formatter='my_formatter')
    lcd.config()

    root = logging.getLogger()
    root.debug("Debug.")
    root.info("Info.")
    root.warning("Warning.")
    root.error("Error.")
    root.critical("Critical.")
    """
    callable_formatter [ 'my_keyword': 'my_value']: root - WARNING - Warning.
    callable_formatter [ 'my_keyword': 'my_value']: root - ERROR - Error.
    callable_formatter [ 'my_keyword': 'my_value']: root - CRITICAL - Critical.
    """
