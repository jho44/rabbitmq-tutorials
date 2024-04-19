import pika
from pika.exchange_type import ExchangeType

# create connection to local rabbitmq msg broker
# if running remote broker, would put in IP addr or dns name here
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

# by not specifying, we get default channel number
channel = connection.channel()

# producer won't declare the queue -- consumers will
# here, producer has no idea what queues are interested in the msgs it'll produce
# instead, create fan-out exchange
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

message = "hello I want to broadcast this message"

channel.basic_publish(exchange='pubsub', routing_key='', body=message)

print(f"send message: {message}")

# don't leave connections hanging around
connection.close()