# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-17 05:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newblog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blog',
            name='readcount',
            field=models.ImageField(default=0, upload_to=''),
        ),
    ]
