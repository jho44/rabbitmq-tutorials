import pika

# create connection to local rabbitmq msg broker
# if running remote broker, would put in IP addr or dns name here
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

# by not specifying, we get default channel number
channel = connection.channel()

channel.queue_declare(queue='letterbox')

message = "hello this is my first message"

# routing key is name of queue
# just using default exchange by inputting the empty str
channel.basic_publish(exchange='', routing_key='letterbox', body=message)

print(f"send message: {message}")

# don't leave connections hanging around
connection.close()