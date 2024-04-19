import pika
import time
import random

def on_message_received(channel, method, properties, body):
  processing_time = random.randint(1, 6)
  print(f"received: {body}, will take {processing_time} to process")
  time.sleep(processing_time)
  # tells broker which msg we want to ack (i.e. the one we just received)
  channel.basic_ack(delivery_tag=method.delivery_tag)
  print("Finished processing the message")

# create connection to local rabbitmq msg broker
# if running remote broker, would put in IP addr or dns name here
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

# by not specifying, we get default channel number
channel = connection.channel()

# safe to do this in both producer and consumer b/c queue_declare is idempotent op
# i.e. wherever it runs first will actually create the queue
# wherever it runs second will be ignored
channel.queue_declare(queue='letterbox')

# qos = quality of service
# prefetch_count=1 means each consumer will only process 1 msg at a time
# if you were to comment out this line, then msgs would be assigned to consumers in round robin fashion
# so if you have 2 consumers, 1 would take the msgs with odd ID and the other would take msgs with even ID
channel.basic_qos(prefetch_count=1)

# don't automatically acknowledge that you've received a message when you pop up from the queue
# instead, manually ack after finishing a task
channel.basic_consume(queue='letterbox', on_message_callback=on_message_received)

print('Starting consuming')

# will block and keep consuming msgs
channel.start_consuming()
