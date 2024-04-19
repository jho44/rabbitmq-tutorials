import pika
from pika.exchange_type import ExchangeType

def on_message_received(channel, method, properties, body):
  print(f"first_consumer: received new message: {body}")

# create connection to local rabbitmq msg broker
# if running remote broker, would put in IP addr or dns name here
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

# by not specifying, we get default channel number
channel = connection.channel()

channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

# server will choose random queue name for us
# exclusive=True means when consumer connection is closed, queue can be deleted
queue = channel.queue_declare(queue='', exclusive=True)

# now bind queue to exchange
# if don't include this, then consumer won't receive msgs b/c pubsub exchange won't know to push msgs to this queue
channel.queue_bind(exchange='pubsub', queue=queue.method.queue)

# auto_ack: automatically acknowledge that you've received a message
channel.basic_consume(queue='', auto_ack=True, on_message_callback=on_message_received)

print('Starting consuming')

# will block and keep consuming msgs
channel.start_consuming()
