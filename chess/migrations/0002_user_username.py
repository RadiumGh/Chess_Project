# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='username', max_length=30),
        ),
    ]
