# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-03-20 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20170319_1455'),
        ('Post', '0038_remove_post_saves'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='attendees',
            field=models.ManyToManyField(blank=True, to='account.Account'),
        ),
    ]