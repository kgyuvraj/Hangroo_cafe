import datetime
import logging
import os

from django.conf import settings
import jinja2

from commons.models import STATUS_ENABLED
from notification import email_client
from notification.models import NotificationChannelSubscription

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

