from kafka import KafkaConsumer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
from textblob import TextBlob
from elasticsearch import Elasticsearch
import sys

topicName="init-topic"
indexName="init-index"

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

# Store tweet and Sentiment in Elasticsearch
# def main():
#     consumer = KafkaConsumer(topicName)
#     for msg in consumer:
#         jsonMsg = json.loads(msg.value)
#         if 'extended_tweet' in jsonMsg:
#             fullText = jsonMsg['extended_tweet']['full_text']
#         else:
#             fullText = ""
#         if fullText != "":
#             sentiment = detectSentiment(fullText)
#             output = "\nTweet Content: " + fullText + " \nSentiment: " + sentiment + " \n\n"
#             print(output)
#             es.index(index=indexName,doc_type="test-type",body={"author":jsonMsg['user']['screen_name'],"sentiment":sentiment,"message":fullText})
def main():
    consumer = KafkaConsumer(topicName)
    for msg in consumer:
        dict_data = json.loads(msg.value)
        tweet = TextBlob(dict_data["text"])
        print(tweet)
        es.index(index="tweet",doc_type="test-type",body={"author":dict_data["user"]["screen_name"],"date":dict_data["created_at"],"message":dict_data["text"]})
        print('\n')

# Consume Data as per the input HashTag
if __name__ == '__main__':
    if len(sys.argv) <2:
        print('Correct Usage: python <filename> <hashtag-without-#>')
        sys.exit()
    else:
        topicName=sys.argv[1]+'-topictest'
        #indexName='tweet'#sys.argv[1]+'-index'
        main()
