#!/bin/bash

# Create the Kafka topic

# brew
# kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# docker
docker exec -it kafka kafka-topics \
  --create \
  --topic test-topic \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

# Run the producer script
python3 producer.py

# # Run the consumer script
# python3 consumer.py
