from kafka import KafkaConsumer

# Create a KafkaConsumer instance to consume messages from 'test-topic'
consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # Read messages from the beginning if no offset is stored
    group_id='test-group'
)

# Print received messages
for message in consumer:
    print(f"Received: {message.value.decode('utf-8')}")
