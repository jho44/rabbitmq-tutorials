import pika

def on_message_received(channel, method, properties, body):
  print(f"received new message: {body}")

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

# auto_ack: automatically acknowledge that you've received a message
channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=on_message_received)

print('Starting consuming')

# will block and keep consuming msgs
channel.start_consuming()
