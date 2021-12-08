'''
Created on May 30, 2019

@author: akshay.gupta
'''

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls.conf import path
from hangroo import settings

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(template_name="registration/logged_out.htm"), name='logout'),

    url('^user/', include('user.urls')),
    url('^rest/', include('rest.urls')),
    url('^order/', include('order.urls')),
    url('^notification/', include('notification.urls')),
    url('^', include('webapp.urls')),
]
