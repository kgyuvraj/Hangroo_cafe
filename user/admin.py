# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from user.models import PhoneOTP, Avatar, \
 Country, Gender, Organisation, Profile, Follower


# Now register the new UserAdmin...
admin.site.register(Profile)
#admin.site.register(PhoneOTP)
#admin.site.register(Avatar)
#admin.site.register(Gender)
admin.site.register(Country)
admin.site.register(Organisation)
#admin.site.register(Follower)


