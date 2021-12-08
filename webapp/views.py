'''
Created on May 30, 2019

@author: akshay.gupta
'''

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import sys

from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import get_messages
from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from commons.exception import CustomException, UNKNOWN_ERROR
from commons.response import BaseResponse
from commons.trace_logger import trace_logger
from user.models import Profile
from order.services import get_pending_order_page_refresh_time,\
    get_pending_item_page_refresh_time, check_if_new_order_item
from order.models import Order, OrderItem
from auditlog.models import LogEntry, LogEntryManager
from inventory.models import Inventory
from webapp.services import get_sale 
from user import services as user_service
import datetime



# logging.basicConfig()
logger = logging.getLogger(__name__)


def handler404(request):
    return render(request, '404.html', status=404)


@trace_logger
def handler500(request):
    logger.error("500 internal server error occurred -- @: " + 
                 str(request.get_full_path()))
    error_message = get_messages(request)
    type, value, tb = sys.exc_info()
    internal_server_error_context = {
        'messages': error_message, 'exception_value': value}
    return render(request, '500.html', internal_server_error_context, status=500)


@trace_logger
def faqs(request):
    return render(request, 'faqs.html')


@trace_logger
def privacy_policy(request):
    return render(request, 'privacy-policy.html')


@permission_classes((IsAuthenticated,))
@login_required
@trace_logger
def index(request):
    try:
        response = BaseResponse().get_base_response()
        response["title"] = "Index Page"
        custom_exception = CustomException()
        
        # ## if user has just logged in and dont have any organisation redirect to welcome page
        user_profile = Profile.objects.filter(user=request.user)
        if not user_profile.exists():
            return welcome(request)
        #else:
        #    return cloud_accounts(request)
    except Exception as e:
        logger.error(e)
        response["status"] = BaseResponse.STATUS_ERROR
        response["error"]["error_code"] = custom_exception.UNKNOWN_ERROR
        response["error"]["error_message"] = custom_exception.get_exception_messsage(response["error"]["error_code"])
    return render(request, 'index.html', response)


@permission_classes((IsAuthenticated,))
@login_required
@trace_logger
def welcome(request):
    try:
        response = BaseResponse().get_base_response()
        response["title"] = "Welcome Page"
        custom_exception = CustomException()
        # ## if user has existing proflie redirect to index page
        user_profile = Profile.objects.filter(user=request.user)
        if user_profile.exists():
            return index(request)
    except Exception as e:
        logger.error(e)
        response["status"] = BaseResponse.STATUS_ERROR
        response["error"]["error_code"] = custom_exception.UNKNOWN_ERROR
        response["error"]["error_message"] = custom_exception.get_exception_messsage(response["error"]["error_code"])
    return render(request, 'welcome.html', response)


@trace_logger
def login(request):
    try:
        response = BaseResponse().get_base_response()
        response["title"] = "Index Page"
        custom_exception = CustomException()
    except Exception as e:
        logger.error(e)
        response["status"] = BaseResponse.STATUS_ERROR
        response["error"]["error_code"] = custom_exception.UNKNOWN_ERROR
        response["error"]["error_message"] = custom_exception.get_exception_messsage(response["error"]["error_code"])
    return render(request, 'registration/login.html', response)


@permission_classes((IsAuthenticated,))
@login_required
@trace_logger
def pending_orders(request):
    try:
        response = BaseResponse().get_base_response()
        response["title"] = "Pending Orders"
        custom_exception = CustomException(UNKNOWN_ERROR)
        from order.services import get_pending_orders
        ## get user profile
        profile = user_service.get_user_profile(request.user)
        if profile:
            # ## if pending orders are there
            pending_orders = get_pending_orders(profile)
            response["pending_orders"] = pending_orders
            
            page_refresh_time = get_pending_order_page_refresh_time()
            response["page_refresh_time"]=page_refresh_time
        else:
            raise CustomException(custom_exception.USER_PROFILE_NOT_FOUND)     
    except Exception as e:
        logger.error(e)
        response["status"] = BaseResponse.STATUS_ERROR
        if custom_exception.get_exception_messsage(e.message):
            response["error"]["error_code"] = e.message
        else:
            response["error"]["error_code"] = custom_exception.UNKNOWN_ERROR
        response["error"]["error_message"] = custom_exception.get_exception_messsage(response["error"]["error_code"])
    
    return render(request, 'dashboard/pending-orders.html', response)

@permission_classes((IsAuthenticated,))
@login_required
@trace_logger
def pending_items(request):
    try:
        response = BaseResponse().get_base_response()
        response["title"] = "Pending Items"
        custom_exception = CustomException(UNKNOWN_ERROR)
        from order.services import get_pending_items
        ## get user profile
        profile = user_service.get_user_profile(request.user)
        if profile:
            # ## if pending orders are there
            pending_items = get_pending_items(profile)
            page_refresh_time = get_pending_item_page_refresh_time()
            new_order_item = check_if_new_order_item(profile)
            response["pending_items"] =  pending_items
            response["new_order"] = new_order_item
            response["page_refresh_time"]=page_refresh_time
        else:
            raise CustomException(custom_exception.USER_PROFILE_NOT_FOUND)     
    except Exception as e:
        logger.error(e)
        response["status"] = BaseResponse.STATUS_ERROR
        if custom_exception.get_exception_messsage(e.message):
            response["error"]["error_code"] = e.message
        else:
            response["error"]["error_code"] = custom_exception.UNKNOWN_ERROR
        response["error"]["error_message"] = custom_exception.get_exception_messsage(response["error"]["error_code"])
    return render(request, 'dashboard/pending-items.html', response)

@permission_classes((IsAuthenticated,))
@login_required
@trace_logger
def default_dashboard(request):
    date = datetime.date.today()
    from_date = date.strftime("%Y-%m-%d")
    return dashboard(request, from_date, from_date)


@permission_classes((IsAuthenticated,))
@login_required
@trace_logger
def dashboard(request, from_date, to_date):
    response = BaseResponse().get_base_response()
    try:
        response["title"] = "Dashboard"
        custom_exception = CustomException(UNKNOWN_ERROR)
        ## get user profile
        profile = user_service.get_user_profile(request.user)
        if profile:
            total_sale = get_sale(profile,from_date, to_date)
            response["total_sale"] = total_sale
            response["from_date"] = from_date    
            response["to_date"] = to_date
        else:
            raise CustomException(custom_exception.USER_PROFILE_NOT_FOUND)     
    except Exception as e:
        logger.error(e)
        response["status"] = BaseResponse.STATUS_ERROR
        if custom_exception.get_exception_messsage(e.message):
            response["error"]["error_code"] = e.message
        else:
            response["error"]["error_code"] = custom_exception.UNKNOWN_ERROR
        response["error"]["error_message"] = custom_exception.get_exception_messsage(response["error"]["error_code"])
    return render(request, 'dashboard/dashboard.html', response)

@permission_classes((IsAuthenticated,))
@login_required
@trace_logger
def redbull_stock(request):
    response = BaseResponse().get_base_response()
    try:
        response["title"] = "Redbull"
    except Exception as e:
        logger.error(e)
        response["error_message"] = "Some Error Occured"
    return render(request, 'dashboard/redbull-stock.html', response)



