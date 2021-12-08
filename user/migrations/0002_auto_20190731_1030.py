'''
Created on 31-Jul-2019

@author: Akshay Kumar Gupta<akshaykumargupta2208@gmail.com>
'''

# Generated by Django 2.2.3 on 2019-07-31 05:00

import json
from django.db import migrations, transaction
from django.contrib.auth.models import User


def create_superuser(apps, schema_editor):
    password = 'DwuzE5kUhcuWbJGd'
    username = 'admin'
    
    User.objects.create_superuser(username=username, password='DwuzE5kUhcuWbJGd', email='admin@hangroo.com')

    print("############# created superuser username : " + username + " password: " + password)


def load_countries(apps, schema_editor):
    print("########## Started loading country data")
    country = apps.get_model('user', 'Country')
    with open('user/migrations/migration_data/country_code.json', 'r') as f:
        json_dict = json.load(f)
    for item in json_dict["countries"]:
        try:
            print("[+] Loading into database : " + item["name"] + "  " + item["code"])
            with transaction.atomic():
                country_object = country(name=item["name"], code=item["code"])
                country_object.save()
        except Exception as e:
            print (e)
            print("[*] Failed to insert into db: " + item["name"] + "  " + item["code"])


def load_genders(apps, schema_editor):
    print("########## Started loading gender data")
    gender = apps.get_model('user', 'Gender')
    with open('user/migrations/migration_data/gender.json', 'r') as f:
        json_dict = json.load(f)
    for item in json_dict["genders"]:
        try:
            print("[+] Loading into database : " + item["name"] + "  " + item["description"])
            with transaction.atomic():
                gender_object = gender(name=item["name"], description=item["description"])
                gender_object.save()
        except Exception as e:
            print (e)
            print("[*] Failed to insert into db: " + item["name"] + "  " + item["description"])


def load_avatars(apps, schema_editor):
    print("########## Started loading avatar data")
    avatar = apps.get_model('user', 'Avatar')
    with open('user/migrations/migration_data/avatar.json', 'r') as f:
        json_dict = json.load(f)
    for item in json_dict["avatars"]:
        try:
            print("[+] Loading into database : " + item["name"] + "  " + item["url"])
            with transaction.atomic():
                avatar_object = avatar(name=item["name"], url=item["url"])
                avatar_object.save()
        except Exception as e:
            print (e)
            print("[*] Failed to insert into db: " + item["name"] + "  " + item["avatar"])

def load_user_data(apps, schema_editor):
    print("########## Started loading users")
    with open('user/migrations/migration_data/users.json', 'r') as f:
        json_dict = json.load(f)
    for item in json_dict:
        try:
            print("[+] Loading into database : " + item + "  " + json_dict[item])
            name_split = json_dict[item].split(" ")
            if len(name_split) > 1:
                first_name = name_split.pop(0)
                last_name = " ".join(name_split).strip()
            else:
                first_name = json_dict[item]
                last_name = ""
            User.objects.create_user(username=item, password='1',first_name=first_name, last_name=last_name)
        except Exception as e:
            print (e)


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_countries),
        migrations.RunPython(load_avatars),
        migrations.RunPython(load_genders),
        migrations.RunPython(create_superuser),
        #migrations.RunPython(load_user_data),
    ]

