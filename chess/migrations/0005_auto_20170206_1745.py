# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0004_auto_20170206_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='loses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
