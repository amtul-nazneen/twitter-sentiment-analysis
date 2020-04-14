from kafka import KafkaConsumer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
from textblob import TextBlob
from elasticsearch import Elasticsearch
es = Elasticsearch()

sid = SentimentIntensityAnalyzer()

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


def main():
    consumer = KafkaConsumer('coronavirus-topic')
    for msg in consumer:
        jsonMsg = json.loads(msg.value)
        if 'extended_tweet' in jsonMsg:
            fullText = jsonMsg['extended_tweet']['full_text']
        else:
            fullText = ""
        if fullText != "":
            sentiment = detectSentiment(fullText)
            output = "\nOriginal Tweet Content: " + fullText + " \nSentiment: " + sentiment + " \n\n"
            #f = open("output.txt", "a+")
            #f.write(output.encode("utf-8"))
            #f.close()
            print(output)
            # tweet = jsonMsg["text"]
            # print("New: ",tweet)
            # tweet = jsonMsg['text']
            print("Author: ",jsonMsg['user']['screen_name'])
            # sentiment2 = detectSentiment(tweet)
            # outputNew = "\nSecond Tweet Content: " + tweet + " \nSentiment: " + sentiment2 + " \n\n"
            es.index(index="covid19",doc_type="test-type",body={"author":jsonMsg['user']['screen_name'],"sentiment":sentiment,"message":fullText})

# def main():
#     consumer = KafkaConsumer('twitter')
#     for msg in consumer:
#         dict_data = json.loads(msg.value)
#         tweet = TextBlob(dict_data["text"])
#         print(tweet)
#         es.index(index="tweet",doc_type="test-type",body={"author":dict_data["user"]["screen_name"],"date":dict_data["created_at"],"message":dict_data["text"]})
#         print('\n')


if __name__ == '__main__':
    main()
