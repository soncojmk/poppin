# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-05 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0029_auto_20161005_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('1', 'Music'), ('2', 'Sports'), ('3', 'Fundraisers'), ('4', 'Dance'), ('5', 'Theatre'), ('6', 'Political'), ('12', 'Movies'), ('7', 'Concerts'), ('8', 'Arts'), ('9', 'Club Event'), ('10', 'Academic'), ('11', 'Professional')], max_length=25, null=True),
        ),
    ]