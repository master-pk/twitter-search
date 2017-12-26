from django.conf.urls import include, url, patterns
from django.contrib import admin

from twitter_local.app import views as twitter_views

urls = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/$', twitter_views.SearchView.as_view()),
)

urlpatterns = patterns(
    '',
    url(r'^', include(urls))
)
