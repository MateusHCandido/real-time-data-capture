from confluent_kafka import Consumer, KafkaError

conf = {
    'bootstrap.servers': 'localhost:9092',  # Replace with actual IP of the Docker host or Kafka container
    'group.id': 'sales_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

# Subscribe to the topic
consumer.subscribe(['sales_topic'])

# Loop to consume messages
try:
    while True:
        msg = consumer.poll(1.0)  # Waits up to 1 second for new messages
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f'End of partition reached {msg.topic()}/{msg.partition()}')
            else:
                print(f'Error: {msg.error()}')
        else:
            print(f"Received message: {msg.value().decode('utf-8')}")  # Print received message

finally:
    # Close the consumer when done
    consumer.close()
