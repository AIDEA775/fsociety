# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 18:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='video',
            name='watchers',
            field=models.ManyToManyField(related_name='watched', through='video.WatchingVideo', to=settings.AUTH_USER_MODEL),
        ),
    ]
