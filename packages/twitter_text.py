def get_tweets(keyword=None, hashtag=None, lang=None):
    # import package
    import tweepy   # extract tweets from Twitter

    # set credentials
    consumer_key = "q1BwFxmCRcLt21Wwx33zXqQVR"   # same as api key
    # same as api secret
    consumer_secret = "rjMIMoYhoOVg6K1wnFEi8vtMtn64hPZChHXDh8JxmcR0Sx9Myg"
    access_key = "1267374302971617282-IB4B6Lfi1QxitPTzw4h5wRRxjjRI6a"
    access_secret = "3iRqJsKLExVAj4tcUoQ0pw3yRAhpBEM1jpcWBvPLzGCfj"

    # Twitter authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # creating an API
    api = tweepy.API(auth)

    print("\n=== tweets ===")
    # query term
    if keyword is not None:
        query_term = keyword
    elif hashtag is not None:
        query_term = "#" + hashtag
    else:   # keyword is None & hashtag is None:
        query_term = "#VaccinationDrive"
    print(f"query_term = {query_term}")
    print(f"lang = {lang}")

    tweets = tweepy.Cursor(
        api.search_tweets, q=query_term, tweet_mode="extended", lang=lang).items(5)   # OPT: compat, lang="en" / "zh"; 1
    return tweets


def get_text(keyword=None, hashtag=None, lang=None):
    tweets = get_tweets(keyword, hashtag, lang)

    text = ""
    for tweet in tweets:
        print(f"IMPORTANT: tweet = {tweet}")
        text += tweet._json["full_text"]
        print("text:", text)

    return text


# TODO: rename "title" to "content"
def get_text_w_title(keyword=None, hashtag=None, lang=None):
    import fugashi
    """ tweets = get_tweets(keyword, hashtag, lang)

    text = ""
    for tweet in tweets:
        print(f"IMPORTANT: tweet = {tweet}")
        text += tweet._json["full_text"]
        print("text:", text) """

    tweets = get_tweets(keyword, hashtag, lang)
    # tweets = ["aaa bbb ccc", "bbb ccc ddd", "eee fff ggg"]
    print(f"tweets = {tweets}")

    count_dict = dict()
    titles_dict = dict()
    # tweet id used to get its url (http://twitter.com/twitter/statuses/{id})
    ids_dict = dict()

    for tweet in tweets:
        """ print(f"tweet = {tweet}")   # D
        print(f"tweet._json = {tweet._json}")
        print(f"tweet._json['full_text'] = {tweet._json['full_text']}")
        print(f"tweet.text = {tweet.text}")
        print(f"tweet.id = {tweet.id}") """

        tweet._json["full_text"]
        text = tweet._json["full_text"]
        id = tweet._json["id_str"]   # id

        # words = text.split()   // ONLY work well in en
        # The Tagger object holds state about the dictionary.
        tagger = fugashi.Tagger()
        words = [word.surface for word in tagger(text)]

        print(text)
        print(words)

        # if (word not in count_dict)
        # count_dict.

        for word in words:
            print(word)
            # count_dict[word] = ((word in count_dict) ? count_dict.get(word) : 0) + 1
            count = 0   # counter start from 0 by default
            titles = list()
            ids = list()

            if (word in count_dict):
                count = count_dict.get(word)
                titles = titles_dict.get(word)
                ids = ids_dict.get(word)

            print("=====")
            print(f"BFR: titles = {titles}")
            titles.append(text)
            ids.append(id)
            print(f"AFR: titles = {titles}")

            count_dict[word] = count + 1
            titles_dict[word] = titles
            ids_dict[word] = ids
            print(f"count_dict = {count_dict}")
            print(f"titles_dict = {titles_dict}")

            out_dict = {
                "count": count_dict,
                "sample_title": titles_dict,
                "ids": ids_dict
            }
            print(f"out_dict = {out_dict}")

    # return text
    return out_dict


def get_refined_tweet_list(keyword=None, hashtag=None):
    import pandas as pd   # make dataframe, export csv
    
    tweets = get_tweets(keyword, hashtag)

    refined_tweet_list = list()
    for tweet in tweets:
        print(f"IMPORTANT: tweet = {tweet}")
        text = tweet._json["full_text"]
        print("text:", text)

        refined_tweet = {'text': text,
                         'favorite_count': tweet.favorite_count,
                         'retweet_count': tweet.retweet_count,
                         'created_at': tweet.created_at}

        refined_tweet_list.append(refined_tweet)
        print("refined_tweet_list:", refined_tweet_list)

    # make a dataframe of tweets with columns representing the different attributes of tweet
    df = pd.DataFrame(refined_tweet_list)
    df.to_csv('refined_tweets.csv')
    print("df:", df)

    # return df
    return refined_tweet_list
