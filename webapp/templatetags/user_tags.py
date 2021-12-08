'''
Created on 06-Aug-2019

@author: akshay.gupta
'''

# Stdlib imports

# Core Django imports
from django import template
from user.models import Profile

# Third-party app imports

# Realative imports of the 'app-name' package

register = template.Library() 


@register.filter(name='has_group') 
def has_group(user, group_name):
    status = False
    if user is not None:
        status = user.groups.filter(name=group_name).exists() 
    return status

@register.filter(name='has_organisation') 
def has_organisation(user):
    status = False
    if user is not None:
        for profile in  Profile.objects.filter(user=user):
            if profile.organisation:
                status = True 
    return status
