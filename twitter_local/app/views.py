from django.shortcuts import render
from rest_framework import (
    exceptions as rest_exceptions,
    permissions as rest_permissions,
    response as rest_response,
    views as rest_views,
)

from twitter_local.app import (
    base as twitter_base,
    serializers as twitter_serializers,
)


class SearchView(rest_views.APIView):

    http_method_names = ['post']
    permission_classes = [rest_permissions.AllowAny]
    filter_serializer_class = twitter_serializers.TweetFilterSerializer

    def post(self, request, *args, **kwargs):
        data = {}
        if request.data:
            filter_serializer = self.filter_serializer_class(data=request.data)
            filter_serializer.is_valid(raise_exception=True)
            search_obj = twitter_base.SearchTwitter()
            data = search_obj.search(filter_serializer.validated_data)
        else:
            raise rest_exceptions.ValidationError('Empty data')

        return rest_response.Response(status=200, data=data)