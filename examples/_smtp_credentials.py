#
# NOTE: EDIT THESE VARIABLES to run the SMTP examples
#

SMTP_USERNAME = 'john.doe'  # assuming your sending email address is
                            # 'john.doe@' + hostname, e.g. 'john.doe@gmail.com'
SMTP_PASSWORD = 'password'  # your password

FROM_ADDRESS = SMTP_USERNAME + '@' + hostname_eg__gmail_dot_com
SMTP_SERVER = tuple_eg__smtp_dot_hostname_comma_TLS_port
# For gmail:
# FROM_ADDRESS =  SMTP_USERNAME + '@gmail.com'
# SMTP_SERVER = ('smtp.gmail.com', 587)
#
# 587 = TLS port
# See http://email.about.com/od/accessinggmail/f/Gmail_SMTP_Settings.htm
