# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170417_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbringitem',
            name='date_time',
            field=models.DateTimeField(null=True),
        ),
    ]
