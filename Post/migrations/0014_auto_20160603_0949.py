# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-03 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0013_auto_20160603_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(default='', upload_to='Post/images/'),
        ),
    ]
