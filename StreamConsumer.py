from kafka import KafkaConsumer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
from textblob import TextBlob
from elasticsearch import Elasticsearch
import sys
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

topicName="init-topic"
indexName="init-index"
kafkaBroker="localhost:9092"
es = Elasticsearch()
sid = SentimentIntensityAnalyzer()

# Analyze the Sentiment
def detectSentiment(sentence):
    compondScore = sid.polarity_scores(sentence)["compound"]
    sentiment = ""
    if compondScore == 0:
        sentiment = "Neutral"
    elif compondScore < 0:
        sentiment = "Negative"
    elif compondScore > 0:
        sentiment = "Positive"
    return sentiment

# Spark Streaming from Kafka Broker
def main():
    sc = SparkContext("local[2]",topicName)
    ssc = StreamingContext(sc, 2)
    kus = KafkaUtils.createDirectStream(ssc,[topicName],{"metadata.broker.list":kafkaBroker})
    output = kus.foreachRDD(connector)
    ssc.start()
    ssc.awaitTermination()

# Store tweet and Sentiment in Elasticsearch
def connector(element):
    alltweets = element.collect()
    for eachtweet in alltweets:
        tweet=eachtweet[1]
        tweet=json.loads(tweet)
        tweet=TextBlob(tweet["text"])
        print("-----------------------------------> Tweet: ",tweet)
        tweet = str(tweet)
        sentiment=detectSentiment(tweet)
        print("-----------------------------------> Sentiment: ",sentiment)
        es.index(index=indexName,doc_type="test-type",body={"sentiment":sentiment,"message":tweet})

#Consume Data as per the input topic
if __name__ == '__main__':
    if len(sys.argv) <2:
        print('Correct Usage: python <filename> <hashtag-without-#>')
        sys.exit()
    else:
        topicName=sys.argv[1]+'-topic'
        indexName=sys.argv[1]+'-index'
        main()
