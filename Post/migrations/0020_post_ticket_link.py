# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-04 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0019_auto_20160928_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ticket_link',
            field=models.URLField(null=True),
        ),
    ]