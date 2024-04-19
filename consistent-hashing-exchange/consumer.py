import pika

def on_message1_received(ch, method, properties, body):
  print(f"queue 1 received new message: {body}")

def on_message2_received(ch, method, properties, body):
  print(f"queue 2 received new message: {body}")

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare("simple-hashing", "x-consistent-hash")

# binding 2 queues to 1 exchange
channel.queue_declare(queue="letterbox-1")
channel.queue_bind("letterbox-1", "simple-hashing", routing_key='1')
channel.basic_consume(
  queue="letterbox-1",
  auto_ack=True,
  on_message_callback=on_message1_received
)

channel.queue_declare(queue="letterbox-2")
channel.queue_bind("letterbox-2", "simple-hashing", routing_key='4')
channel.basic_consume(
  queue="letterbox-2",
  auto_ack=True,
  on_message_callback=on_message2_received
)

print("Starting Consuming")

channel.start_consuming()