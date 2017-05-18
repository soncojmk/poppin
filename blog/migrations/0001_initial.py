# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-02 17:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('image', stdimage.models.StdImageField(blank=True, null=True, upload_to='Post/images')),
                ('posted_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                #('author', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-posted_date'],
            },
        ),
    ]