import json
import logging

import pika

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("amqp")


class AMQPManager:

    def __init__(self, username: str, password: str, host: str, port: int):
        url = "amqp://{}:{}@{}:{}/".format(username, password, host, str(port))
        self.__connection = pika.BlockingConnection(pika.URLParameters(url))

    def publish_message(self, exchange, routing_key, message):
        channel = self.__get_channel()

        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message,
                              properties=pika.BasicProperties(delivery_mode=2))

    def publish_delayed_message(self, exchange, routing_key, data, delay):
        channel = self.__get_channel()
        message = json.dumps(data)
        channel.basic_publish(exchange, routing_key, message,
                              properties=pika.BasicProperties(delivery_mode=2, headers={"x-delay": f"{delay}"}))

    def publish(self, exchange, routing_key, data):
        self.publish_message(exchange, routing_key, json.dumps(data))

    def declare_exchange(self, exchange, exchange_type='topic', durable=True):
        channel = self.__get_channel()
        channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=durable)

    def declare_queue(self, queue_name, exchange, routing_key, durable=True, priority=None):
        channel = self.__get_channel()

        if priority is None:
            channel.queue_declare(queue=queue_name, durable=durable)
        else:
            channel.queue_declare(queue=queue_name, durable=durable, arguments={
                "x-max-priority": priority
            })

        channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)

    def configure_queue(self, exchange, queue_name, routing_key, durable=True,
                        exchange_type='topic',
                        priority=None):

        channel = self.__get_channel()
        _logger.info(f"Declaring exchange {exchange}")

        try:
            if exchange_type == 'x-delayed-message':
                channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=durable,
                                         arguments={"x-delayed-type": "topic"})
            else:
                channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=durable)

            _logger.info(f"Creating {queue_name} queue")
            if priority is None:
                channel.queue_declare(queue=queue_name, durable=durable)
            else:
                channel.queue_declare(queue=queue_name, durable=durable, arguments={
                    "x-max-priority": priority
                })

            channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
            _logger.info('Queue created')
        finally:
            _logger.info(f'Exchange:{exchange_name} declared')
            _logger.info(f'Queue:{queue_name} created & bound with routing key: {routing_key}')
            _logger.info('Connection closed.')

    def __get_channel(self):
        return self.__connection.channel()
