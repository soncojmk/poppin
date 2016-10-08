# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-05 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0027_remove_post_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.IntegerField(choices=[(1, 'Music'), (2, 'Sports'), (3, 'Fundraisers'), (4, 'Dance'), (5, 'Performing Arts'), (6, 'Political'), (7, 'Concerts'), (8, 'Arts'), (9, 'Club Event'), (10, 'Academic'), (11, 'Professional')], default=9, null=True),
        ),
    ]
