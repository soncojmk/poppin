# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-04 21:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0021_auto_20161004_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('CONCERTS', 'Concerts'), ('MUSIC', 'Music'), ('SPORTS', 'Sports'), ('FUNDRAISERS', 'Fundraisers'), ('ARTS', 'Arts'), ('SCIENCE', 'Science'), ('LECTURES', 'Lectures')], default=None, max_length=250)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Post.Category'),
        ),
    ]
