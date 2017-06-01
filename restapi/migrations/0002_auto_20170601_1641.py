# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-01 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='id',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='confirmation_num',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='confirmed',
            field=models.CharField(max_length=20),
        ),
    ]
