import pika

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare("simple-hashing", "x-consistent-hash")

routing_key = "Hash me!"

message = "this is the core message"

channel.basic_publish(
  exchange="simple-hashing",
  routing_key=routing_key,
  body=message
)

print(f"Sent message: {message}")

connection.close()