import json

import unicodecsv
import tempfile

from django.core.files import File
from django.http import HttpResponse
from rest_framework import (
    exceptions as rest_exceptions,
    permissions as rest_permissions,
    response as rest_response,
    views as rest_views,
)

from twitter_local.app import (
    base as twitter_base,
    models as twitter_models,
    serializers as twitter_serializers,
)


class SearchView(rest_views.APIView):

    http_method_names = ['post']
    permission_classes = [rest_permissions.AllowAny]
    filter_serializer_class = twitter_serializers.TweetFilterSerializer

    def post(self, request, *args, **kwargs):
        if request.data:
            filter_serializer = self.filter_serializer_class(data=request.data)
            filter_serializer.is_valid(raise_exception=True)
            search_obj = twitter_base.SearchTwitter()
            data = search_obj.search(filter_serializer.validated_data)

            if filter_serializer.validated_data.get('export'):
                headers = ['twitter_id', 'text', 'date', 'retweet_count']
                # Create results file
                temp_csv_file = tempfile.NamedTemporaryFile(
                    mode='w', prefix='Twitter data', suffix='.csv', delete=False
                )
                writer = unicodecsv.DictWriter(temp_csv_file, fieldnames=headers)
                writer.writeheader()

                for data in twitter_models.Tweets.objects.values('twitter_id', 'text', 'date', 'retweet_count'):
                    writer.writerow({
                        'twitter_id': data['twitter_id']
                    })
                temp_csv_file.flush()
                export_obj = twitter_models.TweetExports(filter=json.dumps(filter_serializer.validated_data))
                export_obj.save('Twitter data', File(open(temp_csv_file.name)))
        else:
            raise rest_exceptions.ValidationError('Empty data')

        return rest_response.Response(status=200, data=data)
