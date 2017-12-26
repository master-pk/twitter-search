from django.contrib import admin

from twitter_local.app import models

admin.site.register(models.Tweets)