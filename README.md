# Twitter Sentimental Analysis
Sentiment analysis of particular hash tags in twitter data in real-time. Here, we do the sentiment analysis for all the tweets for #trump, #coronavirus.

## Framework

#### [SCRAPPER] --> [KAFKA] --> [SPARK STREAMING + SENTIMENT ANALYZER] --> [ELASTICSEARCH] --> [KIBANA]

### Python Scrapper and Kafka
  * The scrapper runs infinitely, collecting all tweets with hashtags with #trump, #coronavirus
  * Sends the collected tweets to Kafka for analytics

### Spark Streaming and Sentimental Analyzer
  * Spark Streaming with a Kafka consumer which periodically collect filtered tweets from the scrapper
  * For each hash tag, perform sentiment analysis using Python Sentiment Analyzing tool - nltk

### Elasticsearch and Kibana
  * Elasticsearch stores the tweets and their sentiment information for further visualization purpose
  * Using Kibana explore the data stored in elasticsearch that shows the tweets' sentiment classification result in a real-time manner

## Prerequisites
1. Kafka with ZooKeeper
2. Elasticsearch
3. Kibana
4. Python 3 and above
5. Twitter API Keys [https://developer.twitter.com/en]

## Server Startup Commands
1. Kafka ZooKeeper: Run the below command from kafka-home
     * `bin/zookeeper-server-start.sh config/zookeeper.properties`
2. Kafka Server: Run the below command from kafka-home
     * `bin/kafka-server-start.sh config/server.properties `
3. List or Delete Kafka topics
     * `bin/kafka-topics.sh --list --zookeeper localhost:2181`
     * `bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic coronavirus-topic`
4. Elasticsearch Server: Run the below command from elasticsearch-home/bin
    * `./elasticsearch`
5. Kibana Server: Run the below command from kibana-home/bin
    * `./kibana`

## Steps to run
1. Run the `StreamProducer.py` by providing the hashtag to analyze
     * Example: `python StreamProducer.py trump`
2. From the spark-home folder, run the `StreamConsumer.py` by providing the hashtag (this is just to open the stream to kafka topic)
     * Example: `bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.1 /path-to-StreamConsumer.py trump`
3. Login to Kibana: http://localhost:5601/ and build visualizations for the below indices that were created
     * coronavirus-index, trump-index

## Visualizations
 * Kibana Visualizations are present in the `kibanaVisuals` folder
 * All visualizations are reported in the `KibanaVisuals.pdf`document in the `kibanaVisuals` folder
