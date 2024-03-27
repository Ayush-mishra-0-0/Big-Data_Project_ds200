#!/bin/bash

cd /usr/local/kafka/
bash -c "bin/zookeeper-server-start.sh config/zookeeper.properties"
