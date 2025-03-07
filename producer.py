import psycopg2 as psy
import select
from confluent_kafka import Producer
import json

conf = {
    'bootstrap.servers': 'localhost:9093',  
}

producer = Producer(conf)


conn = psy.connect(
    dbname='sales_db',
    user='user',
    password='password',
    host='localhost',
    port='5432'
)

conn.autocommit = True
cursor = conn.cursor()

cursor.execute("LISTEN sales_channel;")

while True:
    if select.select([conn], [], [], 5) == ([], [], []):
        continue
    conn.poll()
    while conn.notifies:
        notify = conn.notifies.pop(0)
        print(f'Event receiver: {notify.payload}')
        producer.produce('sales_topic', key='sale', value=notify.payload)
        producer.flush()
