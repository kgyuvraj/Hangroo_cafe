from django.conf.urls import url
from knox import views as knox_views
from rest_framework.documentation import include_docs_urls

from user import views as user_views

urlpatterns = [
   
    url(r'^docs/', include_docs_urls(title='Users API Doc', public=False)),
    url(r'^validate_phone$', user_views.validate_phone_send_otp),
    url(r'^validate_otp$', user_views.validate_otp),
    url(r'^register$', user_views.register_user),
    url(r'^login$', user_views.LoginAPI.as_view()),
    url(r'^logout$', knox_views.LogoutView.as_view()),
    
    url(r'^get_country_list$', user_views.get_country_list),
    url(r'^get_avatar_list$', user_views.get_avatar_list),
    url(r'^get_gender_list$', user_views.get_gender_list),
    url(r'^get_user_profile$', user_views.get_user_profile),
    url(r'^update_user_profile$', user_views.update_user_profile),
    url(r'^get_user_public_info/(?P<username>[\w\-]+)$', user_views.get_user_public_info),
    url(r'^follow_user/(?P<username>[\w\-]+)$', user_views.follow_user),
    url(r'^unfollow_user/(?P<username>[\w\-]+)$', user_views.unfollow_user),
    
    url(r'^report_user$', user_views.report_user),
    url(r'^analyse_all_accounts$', user_views.analyse_all_accounts),
]
