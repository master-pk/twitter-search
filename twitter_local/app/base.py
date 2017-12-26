import datetime
import json

from django.conf import settings
from django.db.models import Q

import twitter

from twitter_local.app import (
    models as twitter_models,
    serializers as twitter_serializers,
)


class SearchTwitter(object):

    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    access_token_key = settings.ACCESS_TOKEN_KEY
    access_token_secret = settings.ACCESS_TOKEN_SECRET

    handler = None

    def authenticate(self):
        self.handler = twitter.Api(consumer_key=self.consumer_key, consumer_secret=self.consumer_secret,
                              access_token_key=self.access_token_key, access_token_secret=self.access_token_secret)

    def search_from_db(self, filter_data):

        filter = Q()

        if filter_data.get('text_type_choice') and filter_data.get('text'):
            if filter_data['text_type_choice'] == 1:
                filter &= Q(text=filter_data['text'])
            elif filter_data['text_type_choice'] == 2:
                filter &= Q(text__startswith=filter_data['text'])
            elif filter_data['text_type_choice'] == 3:
                filter &= Q(text__endswith=filter_data['text'])
            elif filter_data['text_type_choice'] == 4:
                filter &= Q(text__contains=filter_data['text'])

        if filter_data.get('start_date'):
            filter &= Q(date__gte=filter_data['start_date'])

        if filter_data.get('end_date'):
            filter &= Q(date__lte=filter_data['end_date'])

        if filter_data.get('date'):
            filter &= Q(date=filter_data['date'])

        if filter_data.get('lower_retweet_count'):
            filter &= Q(retweet_count__gte=filter_data['lower_retweet_count'])

        if filter_data.get('upper_retweet_count'):
            filter &= Q(retweet_count__lte=filter_data['upper_retweet_count'])

        if filter_data.get('retweet_count'):
            filter &= Q(retweet_count=filter_data['retweet_count'])

        if filter_data.get('is_favorite') is not None:
            filter &= Q(is_favorite=filter_data['is_favorite'])

        return twitter_serializers.TweetFilterSerializer(
            instance=twitter_models.Tweets.objects.filter(filter).order_by(filter_data.get('order_by', '-date')),
            many=True
        ).data

    def format_twitter_data(self, twitter_data):

        return {
            'twitter_id': twitter_data.get('id', ''),
            'text': twitter_data.get('text', ''),
            # NOTE: Python 2 don't have support for formatting the timezone aware string. Currently doing it with replace
            'date': datetime.datetime.strptime(twitter_data['created_at'].replace('+0000', ''), '%a %b %d %H:%M:%S %Y'),
            'retweet_count': twitter_data.get('retweet_count', 0),
            'is_favorite': twitter_data.get('favorited')
        }

    def search(self, filter_data):

        if self.handler is None:
            self.authenticate()

        term = ','.join(filter_data['keywords'])
        since = filter_data.get('start_date')

        data_from_twitter = []

        for tweet_data in self.handler.GetSearch(term=term, since=since, count=100):
            tweet_data = self.format_twitter_data(json.loads(str(tweet_data)))
            data_from_twitter.append(tweet_data)

        existing_twitter_ids = {twitter_id: True for twitter_id in twitter_models.Tweets.objects.values_list('twitter_id', flat=True)}

        # Remove already existing tweets to bulk create rest of new tweets
        data_from_twitter = filter(lambda data: not existing_twitter_ids.get(data['twitter_id']), data_from_twitter)

        # Save newly searched tweets
        twitter_models.Tweets.objects.bulk_create([
            twitter_models.Tweets(**data) for data in data_from_twitter
        ])
        return self.search_from_db(filter_data)
