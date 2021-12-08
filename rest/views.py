'''
Created on May 30, 2019

@author: akshay.gupta
'''

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import threading

from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from commons.response import BaseResponse
from commons.trace_logger import trace_logger
from rest import services


from user.serializers import UserSerializer
from django.contrib.auth.models import User
logger = logging.getLogger(__name__)


# Create your views here.
@trace_logger
def health(request):
    response = BaseResponse().get_base_response()
    try:
        response["title"] = "Health Check"
        response["context"] = "Health OK"
    except Exception as e:
        logger.error(e)
        response["error_message"] = "Some Error Occured"
    return JsonResponse(response)




