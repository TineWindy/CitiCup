# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-15 01:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20180912_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='degree',
            field=models.IntegerField(default=0),
        ),
    ]
