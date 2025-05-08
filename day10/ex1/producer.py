# producer.py
from confluent_kafka import Producer
import json
import time
import pandas as pd

INPUT_FILE_PATH = 'people.csv'

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")

def stream_to_kafka(df):
    config = {
        'bootstrap.servers': 'localhost:9092',
        'enable.idempotence': True,      # Guarantees order even with retries
        'linger.ms': 0,                  # No batching delay
        'acks': 'all',                   # Strong durability
        'max.in.flight.requests.per.connection': 1  # 🧠 CRUCIAL FOR ORDERING
    }
    producer = Producer(config)

    # Send each record to Kafka topic
    print(f"Total messages: {len(df)}")
    for _, row in df.iterrows():
        message = json.dumps(row.to_dict())
        print(f"----- Send message: {message}")
        producer.produce('realtime-data-2', key='sensor-1', value=message, callback=delivery_report)
        producer.poll(0)
    
    # Close producer
    producer.flush()

if __name__ == "__main__":

    # Read CSV into DataFrame
    df = pd.read_csv(INPUT_FILE_PATH)

    stream_to_kafka(df)
