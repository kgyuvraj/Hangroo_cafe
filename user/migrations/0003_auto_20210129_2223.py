# Generated by Django 2.1.15 on 2021-01-29 16:53

import commons.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_auto_20190731_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(1, 'Enable'), (0, 'Disable')], default=1)),
                ('address_line_1', models.TextField(blank=True, max_length=500)),
                ('address_line_2', models.TextField(blank=True, max_length=500)),
                ('remark', models.TextField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_created_by', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'addresss',
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddField(
            model_name='organisation',
            name='address',
            field=models.TextField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.ForeignKey(default='+91', on_delete=django.db.models.deletion.DO_NOTHING, to='user.Country', to_field='code'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.ForeignKey(default='male', on_delete=django.db.models.deletion.DO_NOTHING, to='user.Gender', to_field='name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=enumfields.fields.EnumIntegerField(default=0, enum=commons.models.UserRole),
        ),
    ]
