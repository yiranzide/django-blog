# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-17 05:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newblog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.CharField(max_length=200)),
                ('user_id', models.IntegerField()),
                ('blog_id', models.IntegerField()),
            ],
        ),
    ]
