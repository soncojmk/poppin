# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-19 23:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0004_auto_20170619_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='charge_id',
        ),
    ]
