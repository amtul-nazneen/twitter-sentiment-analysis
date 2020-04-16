from kafka import KafkaProducer
import kafka
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys

# amtul - Twitter API Configurations
consumer_key = "HKZJ3eoU0s60EkMhSWU7fDQ0C"
consumer_secret = "a1YpTw4ntvi2LM7yhWDReIXeCCNVNtCOkLwdeLHWs8Fa3IacTX"
access_token = "979383744627859457-RKRvngKlAGL3SrwKqj64MpOOXcnTF7S"
access_secret = "Gq8nGugfmzdlhrTeiS2PAT2abMgGrdqTWkoFKMSvcx0nU"

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
    topicName=sys.argv[1]+'-topic'
    hashtag='#'+(sys.argv[1])
    print('Hashtag to analyze: ',hashtag)
    twitter_stream.filter(track=[hashtag])
