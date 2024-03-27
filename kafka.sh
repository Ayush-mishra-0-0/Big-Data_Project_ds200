#!/bin/bash


# Start Kafka server
cd /usr/local/kafka/
bash -c "bin/kafka-server-start.sh config/server.properties"
