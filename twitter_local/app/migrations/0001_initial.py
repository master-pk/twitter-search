# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2017, 12, 26, 11, 27, 16, 235070))),
                ('twitter_id', models.CharField(max_length=50)),
                ('retweet_count', models.IntegerField(default=0)),
                ('is_favorite', models.NullBooleanField()),
            ],
        ),
    ]
