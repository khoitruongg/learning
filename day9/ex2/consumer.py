# consumer.py
from confluent_kafka import Consumer, KafkaError
import os
import json
import pandas as pd

output_file = 'output/result.csv'

# Ensure output directory exists
output_dir = os.path.dirname(output_file)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'stream-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['realtime-data'])

messages = []
count = 0
warning_total = 10

with open(output_file, mode='w', newline='') as csvfile:
    writer = None  # Will be initialized after first message

    try:
        while count < warning_total:
            msg = consumer.poll(1.0)  # Poll with 1-second timeout

            if msg is None:
                continue  # No message yet

            if msg.error():
                raise KafkaException(msg.error())

            # Decode and parse the JSON message
            data = json.loads(msg.value().decode('utf-8'))

            messages.append(data)
            count += 1
            print(f"---- Received message #{count}: {data}")

        # Export collected messages to CSV
        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(messages)
        df.to_csv(output_file, index=False)

        print(f"\n Excceed limit {count} items. Result are exporting...")
        print(f"\nExported {count} messages to {output_file}")

    except KeyboardInterrupt:
        print("Stopped by user")

    finally:
        consumer.close()
        print("Kafka consumer closed.")

