'''
Created on May 30, 2019

@author: akshay.gupta
'''
import json
import logging

import requests
from commons.trace_logger import trace_logger

logger = logging.getLogger(__name__)
headers = { 'Content-Type': 'application/json; charset=UTF-8'}


@trace_logger
def notify_google_chat(url, payload):
    logger.debug(url)
    payload = json.dumps(payload)
    logger.debug(payload)
    api_url = url
    response = requests.request("POST", api_url, data=payload, headers=headers)
    return response.text
