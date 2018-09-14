# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-11 16:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import forum.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.IntegerField(choices=[(1, '发帖'), (2, '点赞'), (3, '踩'), (4, '评论')], default=1, verbose_name='operation')),
                ('income', models.FloatField(default=0.0, verbose_name='income')),
                ('tags', models.CharField(default='', max_length=144, verbose_name='tags')),
            ],
        ),
        migrations.CreateModel(
            name='LikeOrDis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userprefer', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=36, verbose_name='postTitle')),
                ('content', models.TextField(default='', verbose_name='postContent')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('viewtimes', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='', verbose_name='postContent')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('userprefer', models.IntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='forum.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=forum.models.get_pyImage_upload_to, verbose_name='PyPostImages')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=36, verbose_name='name')),
                ('info', models.FloatField(default=0.0, verbose_name='info')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='forum.Tag', verbose_name='tags'),
        ),
        migrations.AddField(
            model_name='likeordis',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='forum.Post'),
        ),
        migrations.AddField(
            model_name='likeordis',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likeuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='history',
            name='to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Post', verbose_name='object'),
        ),
        migrations.AddField(
            model_name='history',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='likeordis',
            unique_together=set([('user', 'post')]),
        ),
    ]
