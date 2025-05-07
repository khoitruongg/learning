# producer.py
from confluent_kafka import Producer
from spark_etl import spark_transform
import json
import time

INPUT_FILE_PATH = 'people.csv'

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    # else:
    #     print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def stream_to_kafka(jsonDf, spark):
    producer = Producer({'bootstrap.servers': 'localhost:9092'})

    # Send each record to Kafka topic
     # Send each record to Kafka
    print(f"Total messages: {jsonDf.count()}")
    for row in jsonDf.toLocalIterator():  # More memory-efficient than collect()
        print(f"----- Send message: {row}")
        producer.produce('realtime-data', key='sensor-1', value=row, callback=delivery_report)
        time.sleep(1)
    
    # Close producer
    producer.flush()

    # Stop SparkSession
    spark.stop()

if __name__ == "__main__":
    # Read CSV and get DataFrame
    jsonDf, spark = spark_transform(INPUT_FILE_PATH)
    stream_to_kafka(jsonDf, spark)
