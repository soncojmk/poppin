# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-04 21:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0024_auto_20161004_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Post.Category'),
        ),
    ]