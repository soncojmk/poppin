# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-19 23:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0002_ticket_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='charge_id',
            field=models.CharField(default=datetime.datetime(2017, 6, 19, 23, 39, 28, 569655, tzinfo=utc), max_length=30),
            preserve_default=False,
        ),
    ]