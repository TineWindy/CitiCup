# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-15 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20180915_0323'),
    ]

    operations = [
        migrations.AddField(
            model_name='likeordis',
            name='tags',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='postcomments',
            name='tags',
            field=models.CharField(default='', max_length=128),
        ),
    ]
