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
channel.exchange_declare(exchange='topicexchange', exchange_type=ExchangeType.topic)

user_payments_message = "A european user paid for something"
channel.basic_publish(exchange='topicexchange', routing_key='user.europe.payments', body=user_payments_message)
print(f"send message: {user_payments_message}")

business_order_message = "A european business ordered goods"
channel.basic_publish(exchange='topicexchange', routing_key='business.europe.order', body=business_order_message)
print(f"send message: {business_order_message}")

# don't leave connections hanging around
connection.close()