import boto3
import json
import pika
from abc import ABC, abstractclassmethod
from django.conf import settings


class PublisherBase(ABC):

    @abstractclassmethod
    def publish(cls, topic_name, body):
        pass


class Sqs(PublisherBase):

    @classmethod
    def publish(cls, topic_name, body):
        message_attributes = {
            'routing_key': {
                'StringValue': topic_name,
                'DataType': 'String'
            }
        }
        sqs = boto3.resource('sqs', region_name=settings.AWS_REGION_NAME, aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        queue = sqs.get_queue_by_name(QueueName='ticketo')
        queue.send_message(MessageBody=json.dumps(body), MessageAttributes=message_attributes)


class RabbitMQ(PublisherBase):

    @classmethod
    def publish(cls, topic_name, body):
        print(settings.RABBITMQ_URL)
        params = pika.URLParameters(settings.RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.exchange_declare(exchange=topic_name, exchange_type='topic', durable=True)
        channel.basic_publish(exchange=topic_name, routing_key=topic_name, body=json.dumps(body))


class Publisher:
    SQS = 'SQS'
    RABBITMQ = 'RABBITMQ'

    @staticmethod
    def publish(topic_name, body):
        publishers = {
            Publisher.SQS: Sqs(),
            Publisher.RABBITMQ: RabbitMQ()
        }
        publisher = publishers[settings.BROKER_NAME]
        publisher.publish(topic_name, body)
