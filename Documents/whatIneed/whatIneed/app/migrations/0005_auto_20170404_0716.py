# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 07:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_event_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='friendly_id',
        ),
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]