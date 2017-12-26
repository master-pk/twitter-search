# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TweetExports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filter', models.TextField()),
                ('file', models.FileField(upload_to=b'exports')),
            ],
        ),
        migrations.AlterField(
            model_name='tweets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 26, 11, 59, 58, 577718)),
        ),
    ]
