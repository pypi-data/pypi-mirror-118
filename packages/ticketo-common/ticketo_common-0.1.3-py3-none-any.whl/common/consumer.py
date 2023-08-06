import boto3
import pika
from abc import ABC, abstractclassmethod
from django.conf import settings


class ExchangeBase(ABC):

    @abstractclassmethod
    def get_exchange_methods():
        pass


class ConsumerBase(ABC):

    @abstractclassmethod
    def __init__():
        pass

    @abstractclassmethod
    def consumer_fn():
        pass

    @abstractclassmethod
    def consume(cls):
        pass


class Sqs(ConsumerBase):

    def __init__(self, exchanges):
        self.exchanges = exchanges

    def consumer_fn():
        pass

    def consume(self):
        sqs = boto3.resource('sqs', region_name=settings.AWS_REGION_NAME, aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        queue = sqs.get_queue_by_name(QueueName='ticketo')
        for message in queue.receive_messages(MessageAttributeNames=['routing_key']):
            # QUEUES = {
            #     'ticketo_ticket_created': self.ticket_created,
            #     'ticketo_ticket_updated': self.ticket_updated,
            #     'ticketo_ticket_deleted': self.ticket_deleted
            # }
            # queue_fn = QUEUES[header_frame.content_type]
            # queue_fn(body)
            # print(message.message_attributes)
            pass


class RabbitMQ(ConsumerBase):

    def __init__(self, exchanges):
        self.exchanges = exchanges

    def consumer_fn(self, channel, method_frame, header_frame, body):
        exchange_fn = self.exchanges[method_frame.exchange]
        exchange_fn(body)

    def consume(self):
        params = pika.URLParameters(settings.RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=settings.SERVICE_QUEUE, durable=True)
        channel.basic_consume(queue=settings.SERVICE_QUEUE, on_message_callback=self.consumer_fn, auto_ack=True)
        channel.start_consuming()
        channel.close()


class ConsumerFactory:

    @staticmethod
    def get_consumer(consumer_name, exchanges):
        CONSUMERS = {
            'SQS': Sqs,
            'RABBITMQ': RabbitMQ
        }
        Consumer = CONSUMERS[consumer_name]
        return Consumer(exchanges=exchanges)
