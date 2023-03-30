from rest_framework import serializers
from tweets.models import Tweet


class TweetSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('id',
                  'term',
                  'data')


class TweetDataSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('data')
