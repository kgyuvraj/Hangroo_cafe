# -*- coding: utf-8 -*-
"""
Status Metric:
0 : disabled
1 : enabled
2 : blocked
"""

from __future__ import unicode_literals

import uuid

from auditlog.registry import auditlog
from autoslug.fields import AutoSlugField
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.db import models
from knox.models import AuthToken
from commons.models import STATUS_CHOICES, STATUS_ENABLED, UserRole
from auditlog.models import AuditlogHistoryField
from enumfields import EnumIntegerField

class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255)
    code = models.CharField(unique=True, max_length=255)
    status = models.IntegerField(default=STATUS_ENABLED, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()
    class Meta:
        db_table = 'country'

    def __str__(self):
        return str(self.name)


class Avatar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255)
    avatar_slug = AutoSlugField(populate_from='name')
    url = models.ImageField(blank=True, null=True, upload_to='images/avatar/')
    status = models.IntegerField(default=STATUS_ENABLED, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()
    class Meta:
        db_table = 'avatar'

    def __str__(self):
        return str(self.name)


class Gender(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(default=STATUS_ENABLED, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()
    class Meta:
        db_table = 'gender'

    def __str__(self):
        return str(self.name)


class PhoneOTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format '+919121212121'. upto 14 digits allowed")
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text="Number of Otp sent")
    validated = models.BooleanField(default=False, help_text="If OTP verification got successful")
    forgot = models.BooleanField(default=False, help_text="Only True for forgot password")
    forgot_logged = models.BooleanField(default=False, help_text="Only True if validated otp and forgot get success")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()
    def __str__(self):
        return str(self.phone) + " -- " + str(self.otp)

    class Meta:
        db_table = 'phone_otp'


class Follower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, models.DO_NOTHING, related_name="user")
    follower = models.ForeignKey(User, models.DO_NOTHING, related_name="follower")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()
    class Meta:
        db_table = 'follower'

    def __str__(self):
        return str(self.user) + str(self.follower)


class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(default=STATUS_ENABLED, choices=STATUS_CHOICES)
    name = models.CharField(unique=True, max_length=100, blank=True)
    address = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()
    class Meta:
        db_table = 'organisation'

    def __str__(self):
        return str(self.name)


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=STATUS_ENABLED, choices=STATUS_CHOICES)
    address_line_1 = models.TextField(max_length=500, blank=True)
    address_line_2 = models.TextField(max_length=500, blank=True)
    remark = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='address_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='address_updated_by')
    

    class Meta:
        #abstract = True
        db_table = 'addresss'
        ordering = ('-created_at', )

    def __str__(self):
        return str(self.customer.get_full_name()) + "-" + str(self.id.hex)
    
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format '+919121212121'. upto 14 digits allowed")
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True, null=True, blank=True)
    is_phone_validated = models.BooleanField(default=False)
    country = models.ForeignKey(Country, models.DO_NOTHING, to_field='code', default='+91')
    gender = models.ForeignKey(Gender, models.DO_NOTHING, to_field='name', default='male')
    avatar = models.ForeignKey(Avatar, models.DO_NOTHING)
    organisation = models.ForeignKey(Organisation, models.DO_NOTHING)
    bio = models.TextField(max_length=500, blank=True)
    designation = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = EnumIntegerField(default=UserRole.CUSTOMER, enum=UserRole)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()
    class Meta:
        db_table = 'profile'

    def __str__(self):
        return str(self.user.username)
    

from django.contrib.auth.models import User

def get_name(self):
    return self.username + "-" + self.first_name + " " + self.last_name

User.add_to_class("__str__", get_name)



auditlog.register(PhoneOTP)
auditlog.register(Avatar)
auditlog.register(Country)
auditlog.register(Group)
auditlog.register(Gender)
auditlog.register(AuthToken)
auditlog.register(Follower)
auditlog.register(Organisation)
auditlog.register(Profile)
