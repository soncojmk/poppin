# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-27 17:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0038_auto_20160627_1110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='categories',
            new_name='category',
        ),
    ]
