# Generated by Django 5.0.2 on 2024-08-10 10:54

import datetime
import shortuuid.main
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bongapp', '0054_alter_booking_day_alter_chatgroup_groupname'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='banlist',
            field=models.ManyToManyField(blank=True, related_name='banned_from_groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='booking',
            name='day',
            field=models.DateField(default=datetime.datetime(2024, 8, 10, 16, 24, 7, 326093)),
        ),
        migrations.AlterField(
            model_name='chatgroup',
            name='groupname',
            field=models.CharField(blank=True, default=shortuuid.main.ShortUUID.uuid, max_length=100, unique=True),
        ),
    ]
