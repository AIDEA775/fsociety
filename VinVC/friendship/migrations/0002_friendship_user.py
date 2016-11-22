# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 13:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friendship', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendship',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
