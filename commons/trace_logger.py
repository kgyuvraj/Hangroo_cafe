'''
Created on 03-Jun-2019

@author: akshay.gupta
'''


def trace_logger(fn):
    from functools import wraps
    import logging
    @wraps(fn)
    def wrapper(*args, **kwargs):
        log = logging.getLogger(fn.__name__)
        log.info('Started Executing function %s' % fn.__name__)

        out = fn(*args, **kwargs)

        log.info('Done Executing function %s' % fn.__name__)
        # Return the return value
        return out

    return wrapper