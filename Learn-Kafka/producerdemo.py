import json

import msgpack

from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka.future import log

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

future = producer.send('my-topic', b'raw_bytes')

try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    log.exception()
    pass

print(record_metadata.topic)
print(record_metadata.partition)
print(record_metadata.offset)

producer.send('my-topic', key=b'foo', value=b'bar')

producer = KafkaProducer(value_serializer=msgpack.dumps)
producer.send('msgpack-topic', {'key': 'value'})

producer = KafkaProducer(value_serializer=lambda m:json.dumps(m).encode('ascii'))
producer.send('json-topic', {'key': 'value'})

for _ in range(100):
    producer.send('my-topic', b'msg')

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)

producer.send('my-topic', b'raw_bytes').add_callback(on_send_success).add_errback(on_send_error)

producer.flush()

producer = KafkaProducer(retries=5)