from confluent_kafka import Producer
import random
import time



p = Producer({'bootstrap.servers': 'localhost:9095'})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
some_data_source=["disini", "disana", "disitu",  "tralala", "trilili"]
while True:
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    p.produce('quickstart', random.choice(some_data_source).encode('utf-8'), callback=delivery_report)
    # time.sleep(3)
    p.poll(0)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()