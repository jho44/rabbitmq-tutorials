import pika
from pika.exchange_type import ExchangeType

# create connection to local rabbitmq msg broker
# if running remote broker, would put in IP addr or dns name here
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

# by not specifying, we get default channel number
channel = connection.channel()

# queues declared by consumers so producer doesn't need to
# but DO need to declare exchange
channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)

def message(service):
  return f"This message needs to be routed to {service}"

analytics_message = message("analytics")
channel.basic_publish(exchange='routing', routing_key='analyticsonly', body=analytics_message)
print(f"send message: {analytics_message}")

payments_message = message("payments")
channel.basic_publish(exchange='routing', routing_key='paymentsonly', body=payments_message)
print(f"send message: {payments_message}")

# don't leave connections hanging around
connection.close()