'''
Created on May 30, 2019

@author: akshay.gupta
'''

from django.conf.urls import url
from order import views as order_views

urlpatterns = [
    url('accept_order$', order_views.accept_order),
    url('complete_order_item$', order_views.complete_order_item),
    
    url('get_order_types$', order_views.get_todays_order_types),
    url('get_top_selling_items$', order_views.get_todays_top_selling_items),
    url('get_top_selling_item_category$', order_views.get_todays_top_selling_item_category),
    
    url('get_order_types/(?P<from_date>[\w\-]+)/(?P<to_date>[\w\-]+)$', order_views.get_order_types),
    url('get_top_selling_items/(?P<from_date>[\w\-]+)/(?P<to_date>[\w\-]+)$', order_views.get_top_selling_items),
    url('get_top_selling_item_category/(?P<from_date>[\w\-]+)/(?P<to_date>[\w\-]+)$', order_views.get_top_selling_item_category),
    

    url('print_order/$', order_views.print_order),
    url('print_order/(?P<order_id>[\w\-]+)/$',  order_views.print_order),
    

]
