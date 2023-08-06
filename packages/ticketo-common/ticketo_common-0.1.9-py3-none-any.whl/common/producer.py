import boto3
import json
import pika
from abc import ABC, abstractclassmethod
from django.conf import settings


class PublisherBase(ABC):

    @abstractclassmethod
    def publish(cls, topic_name, body, delay):
        pass


class Sqs(PublisherBase):

    @classmethod
    def publish(cls, topic_name, body, delay):
        sns_client_options = {
            'region_name': settings.AWS_REGION_NAME,
            'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
            'endpoint_url': settings.AWS_ENDPOINT_URL
        }
        sns_client = boto3.client("sns", **sns_client_options)
        sns_client.publish(
            TopicArn=settings.AWS_TOPIC_ARN_BASE + topic_name,
            Subject=topic_name,
            Message=json.dumps(body)
        )


class RabbitMQ(PublisherBase):

    @classmethod
    def publish(cls, topic_name, body, delay):
        params = pika.URLParameters(settings.RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        if delay:
            channel.exchange_declare(exchange=topic_name, exchange_type='x-delayed-message',
                                     arguments={'x-delayed-type': 'direct'})
            properties = pika.BasicProperties(headers={'x-delay': delay})
            channel.basic_publish(exchange=topic_name, routing_key=topic_name, properties=properties,
                                  body=json.dumps(body))
        else:
            channel.exchange_declare(exchange=topic_name, exchange_type='topic', durable=True)
            channel.basic_publish(exchange=topic_name, routing_key=topic_name, body=json.dumps(body))


class Publisher:
    SQS = 'SQS'
    RABBITMQ = 'RABBITMQ'

    @staticmethod
    def publish(topic_name, body, delay=None):
        publishers = {
            Publisher.SQS: Sqs(),
            Publisher.RABBITMQ: RabbitMQ()
        }
        publisher = publishers[settings.BROKER_NAME]
        publisher.publish(topic_name, body, delay)
