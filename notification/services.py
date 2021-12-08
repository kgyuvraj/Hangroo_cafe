'''
Created on 05-Jun-2019

@author: Akshay Kumar Gupta<akshaykumargupta2208@gmail.com>
'''

import logging

from django.conf import settings

from commons.models import STATUS_ENABLED

logger = logging.getLogger(__name__)


##### default logger to log entry and exit of each function
def trace_logger(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        log = logging.getLogger(fn.__name__)
        log.info('Started Executing function %s' % fn.__name__)

        out = fn(*args, **kwargs)

        log.info('Done Executing function %s' % fn.__name__)
        # Return the return value
        return out

    return wrapper


class SMSNotification:
    VERIFICATION_TEMPLATE = " {code} is your account verification code for {app_name}"

    @trace_logger
    def send_verification_code(self, recipient, code):
       pass