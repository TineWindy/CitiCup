# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-14 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20180914_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='useriis',
            name='day',
            field=models.CharField(default='1970-01-01', max_length=128),
        ),
    ]
