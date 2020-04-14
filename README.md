# Twitter Sentimental Analysis
Sentiment analysis of particular hash tags in twitter data in real-time

We want to do the sentiment analysis for all the tweets for #trump, #coronavirus

Framework has the following components

[SCRAPPER] --> [KAFKA] --> [SENTIMENT ANALYZER + SPARK STREAMING] --> [ELASTICSEARCH] --> [KIBANA]


## Python Scrapper and Kafka
  * The scrapper runs infinitely, collecting all tweets with hashtags with #trump, #coronavirus 
  * Sends the collected tweets to Kafka for analytics


## Spark Streaming and Sentimental Analyzer
  * A Kafka consumer which periodically collect filtered tweets from the scrapper
  * For each hash tag, perform sentiment analysis using Python Sentiment Analyzing tool - nltk 

## Elasticsearch and Kibana 
  * Elasticsearch stores the tweets and their sentiment information for further visualization purpose
  * Using Kibana explore the data stored in elasticsearch that shows the tweets' sentiment classification result in a real-time manner
