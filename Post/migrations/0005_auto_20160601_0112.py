# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-01 05:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0004_auto_20160601_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(blank=True),
        ),
    ]
