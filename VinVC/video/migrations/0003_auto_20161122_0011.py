# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 03:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20161121_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchingvideo',
            name='user',
        ),
        migrations.RemoveField(
            model_name='watchingvideo',
            name='video',
        ),
        migrations.RemoveField(
            model_name='video',
            name='watchers',
        ),
        migrations.DeleteModel(
            name='WatchingVideo',
        ),
    ]