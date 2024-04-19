import pika
from pika.exchange_type import ExchangeType

def on_message_received(channel, method, properties, body):
  print(f"Payments Service - received new message: {body}")

# create connection to local rabbitmq msg broker
# if running remote broker, would put in IP addr or dns name here
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

# by not specifying, we get default channel number
channel = connection.channel()

channel.exchange_declare(exchange='topicexchange', exchange_type=ExchangeType.topic)

queue = channel.queue_declare(queue='', exclusive=True)

channel.queue_bind(exchange='topicexchange', queue=queue.method.queue, routing_key='#.payments')

# auto_ack: automatically acknowledge that you've received a message
channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

print('Starting consuming')

# will block and keep consuming msgs
channel.start_consuming()
