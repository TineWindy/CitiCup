# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-30 22:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginuser',
            name='address',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='loginuser',
            name='company',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='loginuser',
            name='job',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='loginuser',
            name='major',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='loginuser',
            name='wealth',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=40, null=True),
        ),
    ]