# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-28 22:07
from __future__ import unicode_literals

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_account_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to='account'),
        ),
    ]