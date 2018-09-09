from prelogging import LCDict
import logging

# TODO --   Revisit once LCDict has ``add_custom_cormatter`` method (use that!)
# #  |      Add to guide-to-examples.rst

KEYWORD = 'my_keyword'

class MyFormatter(logging.Formatter):
    def __init__(self, **kwargs):
        self.value=kwargs.pop(KEYWORD, '')
        kwargs.pop('class', None)
        s = super(MyFormatter, self).__init__(**kwargs)

    def format(self, logrecord, *args, **kwds):
        message = super(MyFormatter, self).format(logrecord, *args, **kwds)
        return 'MyFormatter [%r: %r] says: %s' % (KEYWORD, self.value, message)

# def MyFormatter(**kwargs):
#     return my_callable
#
# def my_callable(logrecord, *args, **kwds):
#     msg = logrecord.message
#     # return 'MyFormatter [%r: %r] says: %s' % (KEYWORD, self.value, msg)
#     return 'my_callable says: %s' % msg

lcd = LCDict(attach_handlers_to_root=True)
lcd.add_formatter('my_formatter',
                  format='%(name)s - %(levelname)s - %(message)s',
                  ** {'()': MyFormatter,
                      KEYWORD: 'my_value'
                      })
lcd.add_stdout_handler('out', formatter='my_formatter')
lcd.config()

root = logging.getLogger()
root.debug("Debug.")
root.info("Info.")
root.warning("Warning.")
root.error("Error.")
root.critical("Critical.")
