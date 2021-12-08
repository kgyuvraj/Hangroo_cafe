'''
Created on 05-Jun-2019

@author: Akshay Kumar Gupta<akshaykumargupta2208@gmail.com>
'''

import logging
import random

import phonenumbers

from commons.exception import CustomException
from commons.models import  STATUS_ENABLED
from commons.response import BaseResponse
from notification.services import SMSNotification
from user.models import PhoneOTP, Avatar, Gender, \
    Country, Profile
from user.serializers import  \
    AvatarSerializer, GenderSerializer, CountrySerializer

# logging.basicConfig()
logger = logging.getLogger(__name__)


def is_phone_valid(phone_number):
    response = False
    if phone_number:
        try:
            phone_obj = phonenumbers.parse(str(phone_number), None)
            if phonenumbers.is_valid_number(phone_obj):
                response = True
        except Exception as e:
            logger.error(e)
    return response


def send_otp(response, phone):
    old = PhoneOTP.objects.filter(phone__iexact=phone)
    if old.exists():
        old = old.first()
        count = old.count
        if count >= 10:
            response["status"] = BaseResponse.STATUS_ERROR
            response["error"]["error_code"] = CustomException.OTP_LIMIT_EXCEEDED 
            response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.OTP_LIMIT_EXCEEDED)
            return response
        key = generate_otp(phone)
        if key:
            old.otp = key
            old.count = count + 1
            old.save()
            response["status"] = BaseResponse.STATUS_SUCCESS
            response["success_message"] = "OTP " + str(key) + " sent Successfully "
        else:
            response["status"] = BaseResponse.STATUS_FAILURE
            response["error"]["error_code"] = CustomException.FAILED_SENDING_OTP 
            response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.FAILED_SENDING_OTP)
    else:
        key = generate_otp(phone)
        if key:
            PhoneOTP.objects.create(
                phone=phone,
                otp=key
            )
            response["status"] = BaseResponse.STATUS_SUCCESS
            response["success_message"] = "OTP " + str(key) + " sent Successfully "
        else:
            response["status"] = BaseResponse.STATUS_ERROR
            response["error"]["error_code"] = CustomException.FAILED_SENDING_OTP 
            response["error"]["error_message"] = CustomException().get_exception_messsage(CustomException.FAILED_SENDING_OTP)
    return response


def generate_otp(phone):
    otp = False
    if phone:
        otp = random.randint(999, 9999)
        try:
            SMSNotification().send_verification_code(phone, otp)
        except Exception as e:
            logger.error(e)
            otp = False
    return otp


def update_user_related_data(response, serializer):    
    avatar = serializer.data.get("avatar", "")
    avatar_serializer = AvatarSerializer(Avatar.objects.filter(pk=avatar).all(), many=True)
    if avatar_serializer.data:
        response["data"]["avatar"] = avatar_serializer.data[0]
    
    gender = serializer.data.get("gender", "")
    gender_serializer = GenderSerializer(Gender.objects.filter(pk=gender).all(), many=True)
    response["data"]["gender"] = gender_serializer.data[0]
    
    country = serializer.data.get("country", "")
    country_serializer = CountrySerializer(Country.objects.filter(pk=country).all(), many=True)
    response["data"]["country"] = country_serializer.data[0]
    return response


def  get_user_profile(user):
    ###check if user has profle
    profile = False
    query_set = Profile.objects.filter(user=user)
    if query_set.exists():
        profile = query_set.first()
    return profile