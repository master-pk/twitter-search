from rest_framework import (
    exceptions as rest_exceptions,
    serializers as rest_serializers,
)

from twitter_local.app import models as twitter_models


class TweetFilterSerializer(rest_serializers.ModelSerializer):

    keywords = rest_serializers.ListField(required=True, write_only=True)
    start_date = rest_serializers.DateField(required=False, write_only=True)
    end_date = rest_serializers.DateField(required=False, write_only=True)
    lower_retweet_count = rest_serializers.IntegerField(required=False, min_value=0, write_only=True)
    upper_retweet_count = rest_serializers.IntegerField(required=False, write_only=True)
    text_type_choice = rest_serializers.ChoiceField(choices=[1, 2, 3, 4], default=1, write_only=True,
                                                    help_text='1 is for exact match, 2 is for starts with, 3 is for ends with and 4 for contains')

    class Meta:
        model = twitter_models.Tweets
        fields = ('text', 'date', 'retweet_count', 'is_favorite', 'start_date', 'end_date', 'lower_retweet_count',
                  'upper_retweet_count', 'text_type_choice', 'keywords', )
        extra_kwargs = {
            'text': {
                'required': False
            },
            'date': {
                'required': False,
            },
            'retweet_count': {
                'required': False,
                'min_value': 0
            },
            'is_favorite': {
                'required': False
            },
        }

    def validate_keywords(self, keywords):
        if len(keywords) == 0:
            raise rest_exceptions.ValidationError('At least one keyword is required')

        return keywords

    def validate(self, attrs):
        if attrs.get('lower_retweet_count') is not None and attrs.get('upper_retweet_count') is not None and attrs.get('retweet_count') is not None:
            raise rest_exceptions.ValidationError('Either give range or exact value')

        if attrs.get('start_date') is not None and attrs.get('end_date') is not None and attrs.get('date') is not None:
            raise rest_exceptions.ValidationError('Either give date range or exact date')

        return attrs
