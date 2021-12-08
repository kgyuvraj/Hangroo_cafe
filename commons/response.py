'''
Created on 03-Jun-2019

@author: akshay.gupta
'''
from django.conf import settings



class BaseResponse():

    BAD_REQUEST = 400
    SUCCESS_CODE = 200
    STATUS_SUCCESS = "success"
    STATUS_FAILURE = "failure"
    STATUS_ERROR = "error"

    def get_base_response(self):
        return  {
            "status": self.STATUS_SUCCESS,
            "success_message": None,
            "data": None,
            "error":{
                "error_message": None,
                "error_code": None,
            },
            "app_version": settings.APP_VERSION
        }
