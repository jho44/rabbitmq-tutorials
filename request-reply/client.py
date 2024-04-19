import pika
import uuid

def on_reply_message_received(channel, method, properties, body):
  print(f"reply received: {body}")

# create connection to local rabbitmq msg broker
# if running remote broker, would put in IP addr or dns name here
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

# by not specifying, we get default channel number
channel = connection.channel()

reply_queue = channel.queue_declare(queue='', exclusive=True)

channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True, on_message_callback=on_reply_message_received)

channel.queue_declare(queue='request-queue', exclusive=True)

message = "Can I request a reply?"

cor_id = str(uuid.uuid4())

print(f"Sending Request: {cor_id}")
# just usin a direct exchange in this example
channel.basic_publish(exchange='', routing_key='request-queue',
                      properties=pika.BasicProperties(
                        reply_to=reply_queue.method.queue,
                        correlation_id=cor_id
                      ),
                      body=message)

print(f'Starting Client')

# will block and keep consuming msgs
channel.start_consuming()
