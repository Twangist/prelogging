#
# NOTE: EDIT THESE VARIABLES to run the SMTP examples
#

# SMTP_USERNAME = 'john.doe'      # assuming your sending email address is 'john.doe@gmail.com'
# SMTP_PASSWORD = 'password'      # your gmail password
SMTP_USERNAME = 'twangist'
SMTP_PASSWORD = '17Frothing71'

FROM_ADDRESS =  SMTP_USERNAME + '@gmail.com'
SMTP_SERVER = ('smtp.gmail.com', 587)
# 587 = TLS port
# See http://email.about.com/od/accessinggmail/f/Gmail_SMTP_Settings.htm
