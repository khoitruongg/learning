from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka import DeserializingConsumer
import time

# Schema Registry configuration
schema_registry_conf = {'url': 'http://localhost:8083'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_deserializer = AvroDeserializer(schema_registry_client)
key_deserializer = StringDeserializer()

consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'key.deserializer': StringDeserializer('utf_8'),
    'value.deserializer': avro_deserializer,
    'group.id': 'user-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
}

consumer = DeserializingConsumer(consumer_conf)
consumer.subscribe(['users'])

# Track the last received time
last_received_time = time.time()

print("Consuming Avro messages...")
while True:
    msg = consumer.poll(timeout=1.0)

    if msg is None:
        # If no message for 30s, close
        # if time.time() - last_received_time > 30:
        #     print("No new message for 30 seconds. Closing consumer.")
        #     break
        continue

    if msg.error():
        print(f"Error: {msg.error()}")
        continue

    # Deserialize the message using AvroDeserializer (done automatically by DeserializingConsumer)
    user_data = msg.value()

    # Check if the deserialization was successful and if the message is valid
    if not user_data:
        print("Error: Failed to deserialize message")
        continue

    # Print the received message
    print(f"Received message: {user_data}")

    # Example: Check if the 'address' field is present in the message
    if 'address' not in user_data:
        print("Warning: Address field is missing")
    else:
        print(f"Address: {user_data['address']}")

    # Track the last received time
    last_received_time = time.time()

consumer.close()
print("Consumer closed.")
