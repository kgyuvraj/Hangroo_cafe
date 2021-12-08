'''
Created on May 30, 2019

@author: akshay.gupta
'''

from django.conf.urls import url
from rest import views as rest_views

urlpatterns = [
    url(r'^health', rest_views.health),

]
