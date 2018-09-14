# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-14 21:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20180909_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserIIS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buys', models.CharField(default='', max_length=2560)),
                ('sells', models.CharField(default='', max_length=2560)),
                ('month_get', models.DecimalField(blank=True, decimal_places=5, max_digits=40, null=True)),
                ('month_rate', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('year_rate', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='loginuser',
            name='alltags',
            field=models.TextField(blank=True, default='{"post":{}, "like":{}, "comment":{}}'),
        ),
        migrations.AddField(
            model_name='loginuser',
            name='forumcoin',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='loginuser',
            name='risk_preference',
            field=models.IntegerField(choices=[(0, 'low'), (1, 'medium'), (2, 'high')], default=0),
        ),
        migrations.AlterField(
            model_name='loginuser',
            name='wealth',
            field=models.DecimalField(blank=True, decimal_places=5, default=0, max_digits=40),
        ),
        migrations.AddField(
            model_name='useriis',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iis', to=settings.AUTH_USER_MODEL),
        ),
    ]
