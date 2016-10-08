# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-05 03:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0025_auto_20161004_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('NOTHING', '------'), ('MUSIC', 'Music'), ('SPORTS', 'Sports'), ('FUNDRAISERS', 'Fundraisers'), ('DANCE', 'Dance'), ('PERFORMING_ARTS', 'Performing Arts'), ('POLITICAL', 'Political'), ('CONCERTS', 'Concerts'), ('ARTS', 'Arts'), ('SCIENCE', 'Science'), ('ACADEMIC', 'Academic'), ('PROFESSIONAL', 'Professional')], default=None, max_length=250),
        ),
    ]
