# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 13:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import video.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('date_upload', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date upload')),
                ('video_file', models.FileField(upload_to='videos/%Y/%m/%d', validators=[video.validators.validate_file_extension])),
                ('thumbnail', models.ImageField(blank=True, upload_to='videos/%Y/%m/%d')),
                ('description', models.CharField(blank=True, default='', max_length=200)),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
