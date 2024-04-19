import pika
import time
import random

# create connection to local rabbitmq msg broker
# if running remote broker, would put in IP addr or dns name here
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

# by not specifying, we get default channel number
channel = connection.channel()

channel.queue_declare(queue='letterbox')

message_id = 1

while True:
  message = f"Sending message_id: {message_id}"

  # routing key is name of queue
  # just using default exchange by inputting the empty str
  channel.basic_publish(exchange='', routing_key='letterbox', body=message)

  print(f"send message: {message}")

  time.sleep(random.randint(1, 4))

  message_id += 1
