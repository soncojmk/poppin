# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-01 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0012_concert_starting_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
    ]