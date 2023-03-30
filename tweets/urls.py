# from django.conf.urls import re_path   # url is deprecated & chg to re_path
from django.urls import re_path
from tweets import views

urlpatterns = [
    re_path(r'^api/tweets$', views.tweet_list),
    re_path(r'^api/tweets/(?P<pk>[0-9]+)$', views.tweet_detail),
    # re_path(r'^api/tweets/published$', views.tweet_list_published)
]
