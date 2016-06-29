# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-28 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0050_remove_eventcomment_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questioncomment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questioncomments', to='Post.Question'),
        ),
    ]
