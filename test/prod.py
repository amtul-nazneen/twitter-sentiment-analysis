from kafka import KafkaProducer
import kafka
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys

# TA - Twitter API Configurations
consumer_key = "XpxjqQ5b4N4qL5dW0L0ZrByUU"
consumer_secret = "OD2pZrQH7BmWd1qPYoeJhKzsfIwwx2DMErckfPAh5PrKoHtbY3"
access_token = "937037281080365056-FBijlyasjMpYnpqHyZaa1IPzLMe4Ze8"
access_secret = "9xY47d5GDz2IdYZbgR3q5uWzQK9XiiFHUiMpruAq7OvsO"

# TWITTER API AUTH
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#Kafka Topic Name for a particular HashTag
topicName="init-topic"

# Twitter Stream Listener
class KafkaPushListener(StreamListener):
    def __init__(self):
        # localhost:9092 = Default Zookeeper Producer Host and Port Adresses
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    def on_data(self, data):
        # Producer produces data for consumer
        self.producer.send(topicName, data.encode('utf-8'))
        #print(data)
        print('Sending data to Kafka.. into topic: ',topicName )
        return True

    def on_error(self, status):
        print(status)
        return True

# Twitter Stream Config
twitter_stream = Stream(auth, KafkaPushListener())

# Produce Data as per the input HashTag
if len(sys.argv) <2:
    print('Correct Usage: python <filename> <hashtag-without-#>')
    sys.exit()
else:
    topicName=sys.argv[1]+'-topictest'
    hashtag='#'+(sys.argv[1])
    print('Hashtag to analyze: ',hashtag)
    twitter_stream.filter(track=[hashtag])
