from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka import SerializingProducer
import uuid
import time

with open("avro/user.avsc", "r") as f:
    schema_str = f.read()

def user_to_dict(user, ctx):
    return user

schema_registry_conf = {'url': 'http://localhost:8083'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_serializer = AvroSerializer(
    schema_registry_client=schema_registry_client,
    schema_str=schema_str,
    to_dict=user_to_dict
)

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': avro_serializer
}

producer = SerializingProducer(producer_conf)

user = {
    "id": str(uuid.uuid4()),
    "name": "Alice",
    "email": "alice@example.com"
}

producer.produce(topic='users', key='user-id', value=user)
print("----- Send Data: ", user)
time.sleep(1)
producer.flush()
