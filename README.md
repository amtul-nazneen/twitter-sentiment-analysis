# Twitter Sentimental Analysis
Sentiment analysis of particular hash tags in twitter data in real-time. Here, we do the sentiment analysis for all the tweets for #trump, #coronavirus.

## Framework

#### [SCRAPPER] --> [KAFKA] --> [SENTIMENT ANALYZER + SPARK STREAMING] --> [ELASTICSEARCH] --> [KIBANA]

### Python Scrapper and Kafka
  * The scrapper runs infinitely, collecting all tweets with hashtags with #trump, #coronavirus
  * Sends the collected tweets to Kafka for analytics

### Spark Streaming and Sentimental Analyzer
  * A Kafka consumer which periodically collect filtered tweets from the scrapper
  * For each hash tag, perform sentiment analysis using Python Sentiment Analyzing tool - nltk

### Elasticsearch and Kibana
  * Elasticsearch stores the tweets and their sentiment information for further visualization purpose
  * Using Kibana explore the data stored in elasticsearch that shows the tweets' sentiment classification result in a real-time manner

## Prerequisites
1. Kafka with ZooKeeper
2. Elasticsearch
3. Kibana
4. Python 3 and above

## Steps to run
1. Run the `StreamProducer.py` by providing the hashtag to analyze
     * Example: `python StreamProducer.py trump`
2. Run the `StreamConsumer.py` by providing the hashtag (this is just to open the stream to kafka topic)
     * Example: `python StreamConsumer.py trump`
3. Login to Kibana: http://localhost:5601/ and build visualizations for the below indices
     * coronavirus-index, trump-index

## Visualizations
 * Kibana Visualizations are present in the `kibanaVisuals` folder
 * All visualizations are reported in the `KibanaVisuals.pdf`document in the `kibanaVisuals` folder
