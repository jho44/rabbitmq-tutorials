import pika
import uuid

def on_request_message_received(channel, method, properties, body):
  print(f"Request received: {properties.correlation_id}")
  # first arg is Exchange
  channel.basic_publish('', routing_key=properties.reply_to, body=f"Hey it's your reply to {properties.correlation_id}")

# create connection to local rabbitmq msg broker
# if running remote broker, would put in IP addr or dns name here
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

# by not specifying, we get default channel number
channel = connection.channel()

channel.queue_declare(queue='request-queue', exclusive=True)

channel.basic_consume(queue='request-queue', auto_ack=True, on_message_callback=on_request_message_received)

print(f'Starting Server')

# will block and keep consuming msgs
channel.start_consuming()
