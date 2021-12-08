'''
Created on 16-Nov-2019

@author: akshay.gupta
'''

import logging

from django.conf import settings
from django.core.mail.message import EmailMessage
import htmlmin

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


@trace_logger
def send_mail_smtp(recipient_list, message_body, subject, attachment=False):
    message_body = htmlmin.minify(message_body)
    msg = EmailMessage(subject, message_body, settings.EMAIL_FROM, recipient_list, bcc=["akshaykumargupta2208@gmail.com"])
    msg.content_subtype = "html"  
    if attachment:
        msg.attach_file(attachment)
    msg.send()


@trace_logger
def send_email(recipient_list, message_body, subject, attachment=False):
    send_mail_smtp(recipient_list, message_body, subject, attachment)
