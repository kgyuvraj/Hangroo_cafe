'''
Created on May 30, 2019

@author: akshay.gupta
'''
import logging
import datetime
from order.models import Order
from django.utils.timezone import make_aware



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




def get_sale(profile, from_date, to_date):
    response = False
    from_date_split = from_date.split("-")
    to_date_split = to_date.split("-")
    start_date = datetime.datetime(year=int(from_date_split[0]), month=int(from_date_split[1]), day=int(from_date_split[2]), hour=0, minute=0, second=0) # represents 00:00:00
    end_date = datetime.datetime(year=int(to_date_split[0]), month=int(to_date_split[1]), day=int(to_date_split[2]), hour=23, minute=59, second=59) # represents 23:59:59
    order_list = Order.objects.filter(updated_at__range=(make_aware(start_date), make_aware(end_date)), organisation=profile.organisation)
    if order_list.exists() :
        cash= 0
        online= 0
        pending = 0
        for order in order_list:
            cash = cash+order.amount_paid_cash
            online = online+order.amount_paid_online
            pending = pending+order.amount_pending
        response = {}
        response["amount_paid_cash"] = cash
        response["amount_paid_online"] = online
        response["amount_pending"] = pending
        response["total_sale"] = cash+online+pending
    return response