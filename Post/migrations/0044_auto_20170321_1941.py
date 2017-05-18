# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-03-21 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0043_auto_20170321_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='attending',
            field=models.ManyToManyField(blank=True, related_name='attending', to='account.Account'),
        ),
    ]