from kafka import KafkaProducer
import kafka
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# TWITTER API CONFIGURATIONS
#consumer_key = "KJEJebQn6alKLIX5woflyzuWh"
#consumer_secret = "rGUwP0y8pYeq0ETBtziebv33FDndK1cyoYSldGRzB9vCkJmwVY"
#access_token = "937037281080365056-FRkTDQYHqrQls6GhWxAKIGuzZ62jvf8"
#access_secret = "1e69BVG27TouAd69360czD9WuTAzMHMrujyHkzv2nILB2"

# TA KEYS
consumer_key = "XpxjqQ5b4N4qL5dW0L0ZrByUU"
consumer_secret = "OD2pZrQH7BmWd1qPYoeJhKzsfIwwx2DMErckfPAh5PrKoHtbY3"
access_token = "937037281080365056-FBijlyasjMpYnpqHyZaa1IPzLMe4Ze8"
access_secret = "9xY47d5GDz2IdYZbgR3q5uWzQK9XiiFHUiMpruAq7OvsO"

# TWITTER API AUTH
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


# Twitter Stream Listener
class KafkaPushListener(StreamListener):
    def __init__(self):
        # localhost:9092 = Default Zookeeper Producer Host and Port Adresses
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])



    def on_data(self, data):
        # Producer produces data for consumer

        self.producer.send("coronavirus-topic", data.encode('utf-8'))
        print(data)
        return True

    def on_error(self, status):
        print(status)
        return True


# Twitter Stream Config
twitter_stream = Stream(auth, KafkaPushListener())

# Produce Data that has Game of Thrones hashtag (Tweets)
twitter_stream.filter(track=['#coronavirus'])
