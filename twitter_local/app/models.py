import datetime

from django.db import models


class Tweets(models.Model):

    text = models.TextField()
    date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    twitter_id = models.CharField(max_length=50)
    retweet_count = models.IntegerField(default=0)
    is_favorite = models.NullBooleanField()

    def __unicode__(self):
        return u'{} - {}'.format(self.text, self.date)


class TweetExports(models.Model):

    filter = models.TextField()
    file = models.FileField(upload_to='exports')
