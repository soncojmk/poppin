# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-30 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0034_auto_20161117_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('1', 'Music'), ('3', 'Fundraisers'), ('13', 'Comedy'), ('14', 'Poetry'), ('4', 'Dance'), ('5', 'Theatre'), ('8', 'Art'), ('6', 'Performing Arts'), ('2', 'Sports'), ('9', 'Club Event'), ('18', 'Debate'), ('17', 'Lecture'), ('10', 'Academic'), ('11', 'Professional'), ('15', 'Other')], max_length=25, null=True),
        ),
    ]