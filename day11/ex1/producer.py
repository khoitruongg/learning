from confluent_kafka import Producer
import time
import json

producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Send 10 example messages
for i in range(10):
    message = {"key": f"key_{i}", "value": f"value_{i}"}
    value_str = json.dumps(message)

    producer.produce('flink-topic',key='test-key', value=value_str)
    print(f"Sent: {message}")
    time.sleep(1)  # Simulate delay between messages

producer.flush()
