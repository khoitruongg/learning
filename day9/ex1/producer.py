import psutil
import json
from kafka import KafkaProducer
import time

# Two producers: one for JSON, one for plain strings
json_producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

string_producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: v.encode('utf-8')
)

# Function to send JSON data
def send_json_data():
    system_data = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent
    }
    json_producer.send('test-topic', value=system_data)
    print("Sent JSON system data:", system_data)
    json_producer.flush()

# Function to send plain string messages
def send_string_messages():
    for i in range(5):
        message = f"Message {i}"
        string_producer.send('test-topic', value=message)
        print(f"Sent: {message}")
        time.sleep(1)
    string_producer.flush()

# Close Producer
def close_producer():
    json_producer.close()
    string_producer.close()

send_json_data()
send_string_messages()
close_producer()

