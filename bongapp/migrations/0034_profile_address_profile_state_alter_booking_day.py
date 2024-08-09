# Generated by Django 5.0.2 on 2024-08-02 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bongapp', '0033_remove_ordermodel_address_remove_ordermodel_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(default='No address', max_length=300),
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.CharField(default='No state', max_length=111),
        ),
        migrations.AlterField(
            model_name='booking',
            name='day',
            field=models.DateField(default=datetime.datetime(2024, 8, 2, 21, 29, 23, 300230)),
        ),
    ]
