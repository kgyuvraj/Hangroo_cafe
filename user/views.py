# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login
from knox.views import LoginView
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commons.response import BaseResponse
from commons.trace_logger import trace_logger
from user import services
from user.models import  PhoneOTP, Gender, \
     Country, Avatar, Follower
from user.serializers import CreateUserSerializer, LoginSerializer, \
    GenderSerializer, \
    UpdateUserSerializer, CountrySerializer, AvatarSerializer,\
    PublicUserSerializer
from user.services import is_phone_valid, send_otp
from commons.exception import CustomException
from django.db.models.query_utils import Q
from django.contrib.auth.models import User
from commons.models import STATUS_DISABLED
import logging
import hangroo.celery

logger = logging.getLogger(__name__)

@api_view(['POST'])
@trace_logger
def validate_phone_send_otp(request):
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
    phone = request.data.get("phone")
    if is_phone_valid(phone):
        phone = str(phone)
        user = User.objects.filter(phone__iexact=phone)
        if user.exists():
            response["status"] = BaseResponse.STATUS_ERROR
            response["error"]["error_code"] =  CustomException.DUPLICATE_PHONE
            response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.DUPLICATE_PHONE)
        else:
            response = send_otp(response, phone)
    else:
        response["status"] = BaseResponse.STATUS_ERROR
        status_code = status.HTTP_400_BAD_REQUEST
        response["error"]["error_code"] = CustomException.INCORRECT_PHONE_NUMBER_FORMAT
        response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.INCORRECT_PHONE_NUMBER_FORMAT)
    
    return Response(response, status=status_code)


@api_view(['POST'])
@trace_logger
def validate_otp(request):
    """
    This will be the second API in the user registration flow.
    
    If you have recieved otp from /user/validate_phone/ api the then send a request with phone and that OTP and you will be eligible for user registration
    
    ## Request Flow :
    phone and OTP as input => api will validate if number and OTP are valid => Confirms the phone number for registration
    
    ## Request Format :
    ```json
    {
        "phone":"+918285XXXXXX",
        "otp": XXXX
    }
    ```
    ## Supported till: 2.0.0
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    phone = request.data.get("phone")
    otp_sent = request.data.get("otp")
    if is_phone_valid(phone) and otp_sent:
        old = PhoneOTP.objects.filter(phone__iexact=phone)
        if old.exists():
            old = old.first()
            otp = old.otp
            if str(otp_sent) == str(otp):
                old.validated = True
                old.save()
                response["status"] = BaseResponse.STATUS_SUCCESS
                response["success_message"] = "OTP matched please proceed for registration"
            else:
                response["status"] = BaseResponse.STATUS_ERROR
                response["error"]["error_code"] = CustomException.OTP_INCORRECT
                response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.OTP_INCORRECT)
        else:
            response["status"] = BaseResponse.STATUS_ERROR
            response["error"]["error_code"] = CustomException.OTP_NOT_SENT 
            response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.OTP_NOT_SENT) 
    else:
        response["status"] = BaseResponse.STATUS_ERROR
        status_code = status.HTTP_400_BAD_REQUEST
        response["error"]["error_code"] = CustomException.OTP_OR_PHONE_INCORRRECT_FORMAT
        response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.OTP_OR_PHONE_INCORRRECT_FORMAT)
    return Response(response, status=status_code)


@api_view(['POST'])
@trace_logger
def register_user(request):
    """
    This will be the third API in the user registration flow.
    
    If you have validated otp from /user/validate_otp/ api then register using this API
    
    ## Request Flow :
    Provide the user details to be registered => api will validate the details => Registers the user
    
    ## Request Format :
    ```json
    {
        "first_name": "",
        "last_name": "",
        "username": "",
        "dob", "YYYY-MM-DD",
        "email": "someemail@gmail.com",
        "phone": "+9182859XXXXX",
        "password":"somestrongpassword",
        "interests": ["<interest_id1>",  "<interest_id2>"],
        "sexual_orientations": ["<sexual_orientation_id1>",  "<sexual_orientation_id2>"],
        "avatar":"avatar_id",
        "gender":"gender_id",
        "country": "country_id",
        "role":"0 for INDIVIDUAL and 1 for BUSINESS"
    }
    ```
    ## Example :
    ```json
    {
    "phone": "+918285922089",
    "password": "1",
    "username": "ad1ada1d",
    "email": "akshay@gmail.com",
    "interests": [
        "ec88108d-04e4-481a-820b-79b5094701db"
    ],
    "dob": "1992-08-22",
    "sexual_orientations": [
        "e260f35a-9d11-456c-b17e-ee5836213d8a"
    ],
    "avatar": "ad6545a5-330b-416d-881d-fcbfe8810b39",
    "gender": "4bbdaafd51eb4058a83f939aefbe3468",
    "country": "1a7ce3f1-49d5-4de4-b6eb-572ca0f8af80",
    "role":0
    }
    ```
    ## Supported till: 1.2.0 
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    phone = request.data.get("phone")
    password = request.data.get("password")
    if is_phone_valid(phone) and password:
        old = PhoneOTP.objects.filter(phone__iexact=phone)
        if old.exists() and old.first().validated:
            serializer = CreateUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response["status"] = BaseResponse.STATUS_SUCCESS
                response["success_message"] = "Account created successfully"
                response["data"] = serializer.data
                
                response = services.update_user_related_data(response, serializer)
                
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                response["status"] = BaseResponse.STATUS_ERROR
                response["error"]["error_code"] = CustomException.SERIALIZER_ERROR
                response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.SERIALIZER_ERROR)
                response["error"]["data"] = serializer.errors
        else:
            response["status"] = BaseResponse.STATUS_ERROR
            response["error"]["error_code"] = CustomException.PHONE_NOT_VALIDATED
            response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.PHONE_NOT_VALIDATED)
    else:
        response["status"] = BaseResponse.STATUS_ERROR
        status_code = status.HTTP_400_BAD_REQUEST
        response["error"]["error_code"] = CustomException.PHONE_OR_PASSWORD_INCORRECT_FORMAT
        response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.PHONE_OR_PASSWORD_INCORRECT_FORMAT) 
    return Response(response, status=status_code)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@trace_logger
def get_user_profile(request):
    """
    This will be will be used to get user details
    
    This API requires authentication
    
    ## Headers Required:
    Authorization : Token <token provided by login API>
    
    ## Request Flow :
    Hit API  => api will validate the provided credentials => API will provide the user details in response
    
    ## Supported till: 2.0.0
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    serializer = CreateUserSerializer(request.user)
    response["data"] = serializer.data
    response = services.update_user_related_data(response, serializer)
    return Response(response, status=status_code)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@trace_logger
def update_user_profile(request):
    """
    This will be will be used to update user details
    
    This API requires authentication
    
    ## Headers Required:
    Authorization : Token <token provided by login API>
    
    ## Request Flow :
    Hit API  => api will validate the provided credentials => api will update the provided details => API will provide the updated user details in response
    ## Request Format :
    ```json
    {
        "first_name": "",
        "last_name": "",
        "username": "",
        "dob", "YYYY-MM-DD",
        "email": "someemail@gmail.com",
        "phone": "+9182859XXXXX",
        "password":"somestrongpassword",
        "interests": ["<interest_id1>",  "<interest_id2>"],
        "sexual_orientations": ["<sexual_orientation_id1>",  "<sexual_orientation_id2>"],
        "avatar":"avatar_id",
        "gender":"gender_id",
        "country": "country_id"
    }
    ```
    ## Example :
    ```json
    {
    "phone": "+918285922089",
    "password": "1",
    "username": "ad1ada1d",
    "email": "akshay@gmail.com",
    "interests": [
        "ec88108d-04e4-481a-820b-79b5094701db"
    ],
    "dob": "1992-08-22",
    "sexual_orientations": [
        "e260f35a-9d11-456c-b17e-ee5836213d8a"
    ],
    "avatar": "ad6545a5-330b-416d-881d-fcbfe8810b39",
    "gender": "4bbdaafd51eb4058a83f939aefbe3468",
    "country": "1a7ce3f1-49d5-4de4-b6eb-572ca0f8af80"
    }
    ```
    ## Only provide the field which you want to update
    ## Supported till: 2.0.0
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    serializer = UpdateUserSerializer(instance=request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        response["status"] = BaseResponse.STATUS_SUCCESS
        response["success_message"] = "Account updated successfully"
        response["data"] = serializer.data
        response = services.update_user_related_data(response, serializer)
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        response["status"] = BaseResponse.STATUS_ERROR
        response["error"]["error_code"] = CustomException.SERIALIZER_ERROR
        response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.SERIALIZER_ERROR)
        response["error"]["data"] = serializer.errors
    return Response(response, status=status_code)


class LoginAPI(LoginView):
    """
    This will be will be used user login to get an authentication token
    
    This API should be used for registered user only
    
    ## Request Flow :
    Provide the user details  => api will validate the details => Provide an authentication token with some additional user details
    
    ## Request Format :
    ```json
    {
        "phone":"+9182859XXXXX",
        "password":"somestrongpassword"
    }    
    ```
    ## Supported till: 2.0.0
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        login_response = LoginView.post(self, request, format=format)
        return login_response


@api_view(['GET'])
@trace_logger
def get_gender_list(request):
    """
    This will be will be used to get all available gender choices
    
    This is an open API and can be hit anonymously.
    
    ## Request Flow :
    Hit API  => api will return all the available gender options
    
    ## Supported till: 2.0.0
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    query_set = Gender.objects.exclude(status=STATUS_DISABLED).all()
    if query_set.exists():
        response["data"] = GenderSerializer(query_set, many=True).data
    return Response(response, status=status_code)


@api_view(['GET'])
@trace_logger
def get_country_list(request):
    """
    This will be will be used to get all available country choices
    
    This is an open API and can be hit anonymously.
    
    ## Request Flow :
    Hit API  => api will return all the available country options
    
    ## Supported till: 2.0.0
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    query_set = Country.objects.exclude(status=STATUS_DISABLED).all()
    if query_set.exists():
        response["data"] = CountrySerializer(query_set, many=True).data
    return Response(response, status=status_code)


@api_view(['GET'])
@trace_logger
def get_avatar_list(request):
    """
    This will be will be used to get all available avatar choices
    
    This is an open API and can be hit anonymously.
    
    ## Request Flow :
    Hit API  => api will return all the available avatar options
    
    ## Supported till: 2.0.0
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    query_set = Avatar.objects.exclude(status=STATUS_DISABLED).all()
    if query_set.exists():
        response["data"] = AvatarSerializer(query_set, many=True).data
    return Response(response, status=status_code)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@trace_logger
def get_user_public_info(request, username):
    """
    This will be will be used to get public details of user by its username
    
    This is an authenticated API and can't be hit anonymously.
    
    ## Request Flow :
    Hit API  => api will return all the available public user data
    
    ## Supported till: 2.0.0
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    query_set = User.objects.filter(username=username)
    if query_set.exists():
        response["data"] = PublicUserSerializer(query_set.first()).data
    else:
        response["status"] = BaseResponse.STATUS_ERROR
        response["error"]["error_code"] = CustomException.USER_DOES_NOT_EXIST
        response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.USER_DOES_NOT_EXIST)
    return Response(response, status=status_code)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@trace_logger
def follow_user(request, username):
    """
    This will be will be used to get all available tag choices
    
    This is an open API and can be hit anonymously.
    
    ## Request Flow :
    Hit API  => api will return all the available avatar options
    
    ## Supported till: 2.0.0
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    # check if user has already liked
    query_set = Follower.objects.filter(Q(follower__id=request.user.id) and Q(user__username=username))
    
    if query_set.exists():
        response["status"] = BaseResponse.STATUS_ERROR
        response["error"]["error_code"] = CustomException.ALREADY_FOLLOWED
        response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.ALREADY_FOLLOWED)
    else:
        user_obj = User.objects.filter(username=username)
        if user_obj.exists():
            follow_obj = Follower()
            follow_obj.follower=request.user
            follow_obj.user = user_obj.first()
            follow_obj.save()
            response["success_message"] = "Followed successfully"
        else:
            response["status"] = BaseResponse.STATUS_ERROR
            response["error"]["error_code"] = CustomException.USER_DOES_NOT_EXIST
            response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.USER_DOES_NOT_EXIST)
    return Response(response, status=status_code)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@trace_logger
def unfollow_user(request, username):
    """
    This will be will be used to get all available tag choices
    
    This is an open API and can be hit anonymously.
    
    ## Request Flow :
    Hit API  => api will return all the available avatar options
    
    ## Supported till: 2.0.0
    """
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    # check if user has already liked
    query_set = Follower.objects.filter(Q(follower__id=request.user.id) and Q(user__username=username))
    
    if query_set.exists():
        query_set.delete()
        response["success_message"] = "Unfollowed successfully"
    else:
        response["status"] = BaseResponse.STATUS_ERROR
        response["error"]["error_code"] = CustomException.USER_DOES_NOT_EXIST
        response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.USER_DOES_NOT_EXIST)
    return Response(response, status=status_code)

def report_user():
    pass

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@trace_logger
def analyse_all_accounts(request):
    status_code = status.HTTP_200_OK
    response = BaseResponse().get_base_response()
    try:
        ### analyse all aws accounts
        aws_accounts = services.get_aws_accounts_by_user(request.user)
        for aws_account in aws_accounts:
            hangroo.celery.analyse_and_notify_all_features_per_account.delay(aws_account.id)
        response["success_message"] = "We are analysing all the components of your cloud, this may take sometime. We will notify you once it is completed."
    except Exception as e:
        logger.error(e)
        response["status"] = BaseResponse.STATUS_ERROR
        response["error"]["error_code"] = CustomException.UNKNOWN_ERROR
        response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.UNKNOWN_ERROR)
    return Response(response, status=status_code)