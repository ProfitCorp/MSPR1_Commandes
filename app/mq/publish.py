import pika
import json
import os

def publish_order_create(data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("MQ_HOST")))
    channel = connection.channel()

    channel.exchange_declare(exchange='orders.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "create",
        "data": data
    })

    channel.basic_publish(exchange='orders.sync', routing_key='', body=message)
    connection.close()


def publish_order_update(order_id: int, data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("MQ_HOST")))
    channel = connection.channel()

    channel.exchange_declare(exchange='orders.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "update",
        "order_id": order_id,
        "data": data
    })

    channel.basic_publish(exchange='orders.sync', routing_key='', body=message)
    connection.close()


def publish_order_delete(order_id: int):
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("MQ_HOST")))
    channel = connection.channel()

    channel.exchange_declare(exchange='orders.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "delete",
        "order_id": order_id,
        "data": {}
    })

    channel.basic_publish(exchange='orders.sync', routing_key='', body=message)
    connection.close()
