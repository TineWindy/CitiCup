# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-15 12:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20180915_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.CharField(default='', max_length=128),
        ),
    ]
