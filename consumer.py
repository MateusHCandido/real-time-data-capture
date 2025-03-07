from confluent_kafka import Consumer, KafkaError

conf = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'sales_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

consumer.subscribe(['sales_topic'])

try:
    while True:
        msg = consumer.poll(1.0)  
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f'End of partition reached {msg.topic()}/{msg.partition()}')
            else:
                print(f'Error: {msg.error()}')
        else:
            print(f"Received message: {msg.value().decode('utf-8')}")  

finally:
    consumer.close()
