# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 05:43
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('title', models.CharField(max_length=4000)),
                ('fetcher', models.CharField(max_length=4000)),
                ('link', models.CharField(max_length=4000)),
                ('description', models.CharField(max_length=4000)),
            ],
        ),
        migrations.CreateModel(
            name='FeedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=4000)),
                ('publish_date', models.DateTimeField()),
                ('link', models.CharField(max_length=4000)),
                ('description', models.TextField()),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yyfeed.Feed')),
            ],
        ),
        migrations.AlterIndexTogether(
            name='feeditem',
            index_together={('feed', 'item_id')},
        ),
    ]
