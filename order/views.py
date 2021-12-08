from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commons.exception import CustomException, UNKNOWN_ERROR
from commons.models import OrderStatus, OrderItemStatus
from commons.response import BaseResponse
from commons.trace_logger import trace_logger
from order.models import Order, OrderItem
import datetime
from django.utils.timezone import make_aware
from django.db.models.aggregates import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from order import services
from user import services as user_service

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@trace_logger
def accept_order(request):
    """
    This will be the first API in the user registration flow.
    
    This API will accept a phone number as input and will send an OTP for phone validation on the same number
    
    ## Request Flow :
    phone as input => api will validate if number is not already registered => send an OTP to the provided phone number
    
    ## Request Format :
    ```json
    {
        "phone":"+9182859222811"
    }
    ```
    ## Supported till: 2.0.0
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    order_id = request.data.get("order_id", None)
    if order_id :
        order = Order.objects.filter(id=order_id)
        if order.exists():
            order = order.first()
            order.status = OrderStatus.PENDING
            order.save()
            response["status"] = BaseResponse.STATUS_SUCCESS
            response["success_message"] = "Order accepted"
        else:
            response["status"] = BaseResponse.STATUS_ERROR
            status_code = status.HTTP_400_BAD_REQUEST
            response["error"]["error_code"] = CustomException.INVALID_ORDER_ID
            response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.INCORRECT_EMAIL_ID)
    else:
        response["status"] = BaseResponse.STATUS_ERROR
        status_code = status.HTTP_400_BAD_REQUEST
        response["error"]["error_code"] = CustomException.INCORRECT_EMAIL_ID
        response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.INCORRECT_EMAIL_ID)
    
    return Response(response, status=status_code)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@trace_logger
def complete_order_item(request):
    """
    This will be the first API in the user registration flow.
    
    This API will accept a phone number as input and will send an OTP for phone validation on the same number
    
    ## Request Flow :
    phone as input => api will validate if number is not already registered => send an OTP to the provided phone number
    
    ## Request Format :
    ```json
    {
        "phone":"+9182859222811"
    }
    ```
    ## Supported till: 2.0.0
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    order_item_id = request.data.get("order_item_id", None)
    if order_item_id :
        order_item = OrderItem.objects.filter(id=order_item_id)
        if order_item.exists():
            order_item = order_item.first()
            order_item.status = OrderItemStatus.COMPLETED
            order_item.save()
            response["status"] = BaseResponse.STATUS_SUCCESS
            response["success_message"] = "Order item completed"
        else:
            response["status"] = BaseResponse.STATUS_ERROR
            status_code = status.HTTP_400_BAD_REQUEST
            response["error"]["error_code"] = CustomException.INVALID_ORDER_ID
            response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.INCORRECT_EMAIL_ID)
    else:
        response["status"] = BaseResponse.STATUS_ERROR
        status_code = status.HTTP_400_BAD_REQUEST
        response["error"]["error_code"] = CustomException.INCORRECT_EMAIL_ID
        response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.INCORRECT_EMAIL_ID)
    
    return Response(response, status=status_code)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@trace_logger
def get_todays_order_types(request):
    date = datetime.date.today()
    from_date = date.strftime("%Y-%m-%d")
    return get_filtered_order_types(request, from_date, from_date)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@trace_logger
def get_order_types(request, from_date, to_date):
    return get_filtered_order_types(request, from_date, to_date)
    
def get_filtered_order_types(request, from_date, to_date):
    try:
        status_code = status.HTTP_200_OK
        response = BaseResponse().get_base_response()
        custom_exception = CustomException(UNKNOWN_ERROR)
        profile = user_service.get_user_profile(request.user)
        if profile:        
            from_date_split = from_date.split("-")
            to_date_split = to_date.split("-")
            start_date = datetime.datetime(year=int(from_date_split[0]), month=int(from_date_split[1]), day=int(from_date_split[2]), hour=0, minute=0, second=0) # represents 00:00:00
            end_date = datetime.datetime(year=int(to_date_split[0]), month=int(to_date_split[1]), day=int(to_date_split[2]), hour=23, minute=59, second=59) # represents 23:59:59
            order_type_data = []
            order_list = Order.objects.filter(organisation=profile.organisation,updated_at__range=(make_aware(start_date), make_aware(end_date))).values('order_type').annotate(total=Count('order_type')).order_by()
            for order in order_list:
                data = [order.get("order_type").name,order.get("total")]
                order_type_data.append(data)
            response["data"] = order_type_data
        else:
            raise CustomException(custom_exception.USER_PROFILE_NOT_FOUND) 
    except Exception as e:
        response["error"]["error_message"] = "Some Error Occured"
    return Response(response, status=status_code)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@trace_logger
def get_todays_top_selling_items(request):
    date = datetime.date.today()
    from_date = date.strftime("%Y-%m-%d")
    return get_filtered_top_selling_items(request, from_date, from_date)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@trace_logger
def get_top_selling_items(request, from_date, to_date):
    return get_filtered_top_selling_items(request, from_date, to_date)

def get_filtered_top_selling_items(request, from_date, to_date):
    try:
        status_code = status.HTTP_200_OK
        response = BaseResponse().get_base_response()
        custom_exception = CustomException(UNKNOWN_ERROR)
        profile = user_service.get_user_profile(request.user)
        if profile:   
            from_date_split = from_date.split("-")
            to_date_split = to_date.split("-")
            start_date = datetime.datetime(year=int(from_date_split[0]), month=int(from_date_split[1]), day=int(from_date_split[2]), hour=0, minute=0, second=0) # represents 00:00:00
            end_date = datetime.datetime(year=int(to_date_split[0]), month=int(to_date_split[1]), day=int(to_date_split[2]), hour=23, minute=59, second=59) # represents 23:59:59
            order_item_data = [["Item", "Qty"]]
            order_item_dict = {}
            order_item_list = OrderItem.objects.filter(order__organisation=profile.organisation,updated_at__range=(make_aware(start_date), make_aware(end_date)),status=OrderItemStatus.COMPLETED).values('product__name', 'qty', ).order_by()
            for order_item in order_item_list:
                if order_item["product__name"] in order_item_dict:
                    order_item_dict[order_item["product__name"]] = order_item_dict[order_item["product__name"]]+order_item["qty"]
                else:
                    order_item_dict[order_item["product__name"]] = order_item["qty"]
            order_item_dict = dict(sorted(order_item_dict.items(), key=lambda item: item[1]))
            for order_item in order_item_dict:
                order_item_data.append([order_item, order_item_dict[order_item]])
            response["data"] = order_item_data
        else:
            raise CustomException(custom_exception.USER_PROFILE_NOT_FOUND) 
    except Exception as e:
        response["error"]["error_message"] = "Some Error Occured"
    return Response(response, status=status_code)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@trace_logger
def get_todays_top_selling_item_category(request):
    date = datetime.date.today()
    from_date = date.strftime("%Y-%m-%d")
    return get_filtered_top_selling_item_category(request, from_date, from_date)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@trace_logger
def get_top_selling_item_category(request, from_date, to_date):
    return get_filtered_top_selling_item_category(request, from_date, to_date)

def get_filtered_top_selling_item_category(request, from_date, to_date):
    try:
        status_code = status.HTTP_200_OK
        response = BaseResponse().get_base_response()
        custom_exception = CustomException(UNKNOWN_ERROR)
        profile = user_service.get_user_profile(request.user)
        if profile:
            from_date_split = from_date.split("-")
            to_date_split = to_date.split("-")
            start_date = datetime.datetime(year=int(from_date_split[0]), month=int(from_date_split[1]), day=int(from_date_split[2]), hour=0, minute=0, second=0) # represents 00:00:00
            end_date = datetime.datetime(year=int(to_date_split[0]), month=int(to_date_split[1]), day=int(to_date_split[2]), hour=23, minute=59, second=59) # represents 23:59:59
            order_item_data = [["Product Category", "Qty"]]
            order_item_dict = {}
            order_item_list = OrderItem.objects.filter(order__organisation=profile.organisation,updated_at__range=(make_aware(start_date), make_aware(end_date)),status=OrderItemStatus.COMPLETED).values('product__category', 'qty', ).order_by()
            for order_item in order_item_list:
                if order_item["product__category"] in order_item_dict:
                    order_item_dict[order_item["product__category"]] = order_item_dict[order_item["product__category"]]+order_item["qty"]
                else:
                    order_item_dict[order_item["product__category"]] = order_item["qty"]
            order_item_dict = dict(sorted(order_item_dict.items(), key=lambda item: item[1]))
            for order_item in order_item_dict:
                order_item_data.append([order_item, order_item_dict[order_item]])
            response["data"] = order_item_data
        else:
            raise CustomException(custom_exception.USER_PROFILE_NOT_FOUND)
    except Exception as e:
        response["error"]["error_message"] = "Some Error Occured"
    return Response(response, status=status_code)


@permission_classes((IsAuthenticated,))
@login_required
@trace_logger
def print_order(request, order_id):
    response = BaseResponse().get_base_response()
    try:
        response["title"] = "Receipt"
        receipt_data = services.get_receipt_data(order_id)
        response["receipt_data"] = receipt_data
        #print(json.dumps(response, indent=4, sort_keys=True, default=uuid_convert))
    except Exception as e:
        #logger.error(e)
        response["error_message"] = "Some Error Occured"
    return render(request, 'print/receipt.html', response)



