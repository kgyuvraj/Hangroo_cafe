'''
Created on May 30, 2019

@author: akshay.gupta
'''

from django.conf.urls import url
from webapp import views as webapp_views

urlpatterns = [
    url(r'^$', webapp_views.pending_orders),
    url('faqs$', webapp_views.faqs),
    url('privacy-policy$', webapp_views.privacy_policy),
    url('pending-orders$', webapp_views.pending_orders),
    url('pending-items$', webapp_views.pending_items),
    url('dashboard$', webapp_views.default_dashboard),
    url('dashboard/(?P<from_date>[\w\-]+)/(?P<to_date>[\w\-]+)$', webapp_views.dashboard),
    url('redbull-stock$', webapp_views.redbull_stock),    
    url('login$', webapp_views.login),

]
