# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-02 03:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0004_remove_eventcomment_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(blank=True, choices=[('1', 'Music'), ('3', 'Fundraisers'), ('13', 'Comedy'), ('14', 'Poetry'), ('4', 'Dance'), ('19', 'Health/Wellbeing'), ('5', 'Theatre'), ('8', 'Art'), ('12', 'Films'), ('6', 'Performing Arts'), ('2', 'Sports'), ('21', 'Political'), ('18', 'Debate'), ('20', 'Gaming'), ('17', 'Lecture'), ('10', 'Academic'), ('11', 'Professional'), ('15', 'Other')], max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
