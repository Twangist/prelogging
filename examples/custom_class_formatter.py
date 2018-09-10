from prelogging import LCDict
import logging

KEYWORD = 'my_keyword'

# "class formatter"

class MyFormatter(logging.Formatter):
    def __init__(self, **kwargs):
        self.value=kwargs.pop(KEYWORD, '')
        kwargs.pop('class', None)
        s = super(MyFormatter, self).__init__(**kwargs)

    def format(self, logrecord, *args, **kwds):
        message = super(MyFormatter, self).format(logrecord, *args, **kwds)
        return 'MyFormatter [%r: %r] says: %s' % (KEYWORD, self.value, message)


if __name__ == '__main__':
    lcd = LCDict(attach_handlers_to_root=True)
    lcd.add_formatter( 'my_formatter',
                       format='%(name)s - %(levelname)s - %(message)s',
                       # dateformat=...,
                       # style=?,
                       ** {'()': MyFormatter,
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
    MyFormatter ['my_keyword': 'my_value'] says: root - WARNING - Warning.
    MyFormatter ['my_keyword': 'my_value'] says: root - ERROR - Error.
    MyFormatter ['my_keyword': 'my_value'] says: root - CRITICAL - Critical.
    """
