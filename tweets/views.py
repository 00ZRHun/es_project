from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from tweets.models import Tweet
from tweets.serializers import TweetSerializers
from rest_framework.decorators import api_view

# Create your views here.


@api_view(['GET', 'POST', 'DELETE'])
def tweet_list(request):
    # GET list of tweets, POST a new tweet, DELETE all tweets

    # retrieve objects (with condition)
    # retrieve all Tweets / find by term from PostgreSQL database
    if request.method == 'GET':
        tweets = Tweet.objects.all()

        term = request.GET.get('term', None)
        if term is not None:
            # partial value (similar to same)
            tweets = tweets.filter(term__icontains=term)

        tweets_serializers = TweetSerializers(tweets, many=True)
        return JsonResponse(tweets_serializers.data, safe=False)
        # 'safe=False' for objects serialization

    # create a new object
    # create and save a new Tweet
    elif request.method == 'POST':
        tweet_data = JSONParser().parse(request)
        tweet_serializer = TweetSerializers(data=tweet_data)
        if (tweet_serializer.is_valid()):
            tweet_serializer.save()
            return JsonResponse(tweet_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete all objects
    # delete all Tweets from database
    elif request.method == 'DELETE':
        count = Tweet.objects.all().delete()
        print(f"count = {count}")   # DEBUG
        return JsonResponse({'message': '{} Tweets were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def tweet_detail(request, pk):
    # ... tweet = Tweet.objects.get(pk=pk)
    # ...
    # find tweet by pk (id)
    try:
        tweet = Tweet.objects.get(pk=pk)
    except Tweet.DoesNotExist:
        return JsonResponse({'message': 'The tweet does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # retrieve a single object
    # find a single Tweet with an id
    if request.method == 'GET':
        tweet_serializer = TweetSerializers(tweet)
        return JsonResponse(tweet_serializer.data)

    # update an object
    # update a Tweet by the id in the request
    elif request.method == 'PUT':
        tweet_data = JSONParser().parse(request)
        tweet_serializer = TweetSerializers(tweet, data=tweet_data)
        if tweet_serializer.is_valid():
            tweet_serializer.save()
            return JsonResponse(tweet_serializer.data)
        return JsonResponse(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def tweet_detail(request, pk):
    #  GET / PUT / DELETE tweet
    # ... tweet = Tweet.objects.get(pk=pk)
    # ...
    # find tweet by pk (id)
    try:
        tweet = Tweet.objects.get(pk=pk)
    except Tweet.DoesNotExist:
        return JsonResponse({'message': 'The tweet does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # retrieve a single object
    # find a single Tweet with an id
    if request.method == 'GET':
        tweet_serializer = TweetSerializers(tweet)
        return JsonResponse(tweet_serializer.data)

    # update an object
    # update a Tweet by the id in the request
    elif request.method == 'PUT':
        tweet_data = JSONParser().parse(request)
        tweet_serializer = TweetSerializers(tweet, data=tweet_data)
        if tweet_serializer.is_valid():
            tweet_serializer.save()
            return JsonResponse(tweet_serializer.data)
        return JsonResponse(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete an object
    # delete a Tweet with the specified id
    elif request.method == 'DELETE':
        tweet.delete()
        return JsonResponse({'message': 'Tweet was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


""" @api_view(['GET'])
def tweet_list_published(request):
    # GET all published tweets
    tweets = Tweet.objects.filter(published=True)

    # find all objects by condition
    # find all objects with published = True
    if request.method == 'GET':
        tweets_serializers = TweetSerializers(tweets, many=True)
        return JsonResponse(tweets_serializers.data, safe=False) """

# v1 api for getTweetByTerm
@api_view(['GET', 'POST', 'DELETE'])
def tweet_list_v1(request):
    # GET list of tweets, POST a new tweet, DELETE all tweets

    # retrieve objects (with condition)
    # retrieve all Tweets / find by term from PostgreSQL database
    if request.method == 'GET':
        tweets = Tweet.objects.all()

        term = request.GET.get('term', None)
        if term is not None:
            # complate value (exactly same), else recreate new obj
            # OPT: term__icontains=term
            tweets = tweets.filter(term=term)

            # if empty, then create a new obj
            # IN
            # print(f"tweets = {tweets}")
            # print(f"tweets.__sizeof__ = {tweets.__sizeof__}")
            # print(f"len(tweets) = {len(tweets)}")
            # print(f"term = {term}")
            # OUT
            # tweets = <QuerySet []>
            # tweets.__sizeof__ = <built-in method __sizeof__ of QuerySet object at 0x7fd6dd9105e0>
            # len(tweets) = 0
            # term = あんスタ
            if len(tweets) < 1:
                # create a new object
                # create and save a new Tweet

                # tweet_data = JSONParser().parse(request)
                tweet_data = dict()
                # OPT: #あんスタ, #あんスタウェルカム祭, #はじめてさんいらっしゃ〜い
                data = get_tweet_text(None, term, "ja")
                tweet_data["term"] = term
                tweet_data["data"] = data
                # print(f"tweet_data = {tweet_data}")   # D

                tweet_serializer = TweetSerializers(data=tweet_data)
                # print(f"tweet_serializer = {tweet_serializer}")   # D

                if (tweet_serializer.is_valid()):
                    tweet_serializer.save()
                    return JsonResponse(tweet_serializer.data, status=status.HTTP_201_CREATED)
                return JsonResponse(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tweets_serializers = TweetSerializers(tweets, many=True)

        # TODO: CAN't WORK: tweets_serializers.data["data"] / .get()
        # print(f"tweets_serializers = {tweets_serializers}")

        # print(f'tweets = {tweets}')
        # print(f'getattr(tweets, "data") = {getattr(tweets, "data")}')
        return JsonResponse(tweets_serializers.data, safe=False)
        # 'safe=False' for objects serialization


# _v1 Reusable / small function(s)
def get_tweet_text(keyword=None, hashtag=None, lang=None):   # hashtag=アンスタ

    from packages.twitter_text import get_text_w_title
    text = get_text_w_title(keyword, hashtag, lang)
    return text
