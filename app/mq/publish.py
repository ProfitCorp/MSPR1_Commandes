import pika
import json

def publish_order_create(data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='orders.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "create",
        "data": data
    })

    channel.basic_publish(exchange='orders.sync', routing_key='', body=message)
    print(f" [x] Création envoyée : {message}")
    connection.close()


def publish_order_update(order_id: int, data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='orders.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "update",
        "order_id": order_id,
        "data": data
    })

    channel.basic_publish(exchange='orders.sync', routing_key='', body=message)
    print(f" [x] Mise à jour envoyée : {message}")
    connection.close()


def publish_order_delete(order_id: int):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='orders.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "delete",
        "order_id": order_id,
        "data": {}
    })

    channel.basic_publish(exchange='orders.sync', routing_key='', body=message)
    print(f" [x] Suppression envoyée : {message}")
    connection.close()

def publish_stock_update(stock_data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='stock.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "stock_update",
        "data": stock_data
    })

    channel.basic_publish(exchange='stock.sync', routing_key='', body=message)
    print(f" [x] Stock update envoyée : {message}")
    connection.close()
