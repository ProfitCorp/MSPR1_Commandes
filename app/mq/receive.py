import pika
import json

def setup_consumer(exchange_name: str, queue_name: str, callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # Déclare l'exchange et la queue
    channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    return channel, connection


def user_callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        action = data.get("action")
        user_id = data.get("user_id")
        user_data = data.get("data", {})

        if action == "create":
            print(f"[User] Création reçue : ID {user_id} — {user_data}")
        elif action == "update":
            print(f"[User] Mise à jour reçue : ID {user_id} — {user_data}")
        elif action == "delete":
            print(f"[User] Suppression reçue : ID {user_id}")
        else:
            print(f"[User] Action inconnue : {data}")
    except json.JSONDecodeError:
        print("[User] Erreur de parsing JSON")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def product_callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        action = data.get("action")
        product_id = data.get("product_id")
        product_data = data.get("data", {})

        if action == "create":
            print(f"[Product] Création reçue : ID {product_id} — {product_data}")
        elif action == "update":
            print(f"[Product] Mise à jour reçue : ID {product_id} — {product_data}")
        elif action == "delete":
            print(f"[Product] Suppression reçue : ID {product_id}")
        else:
            print(f"[Product] Action inconnue : {data}")
    except json.JSONDecodeError:
        print("[Product] Erreur de parsing JSON")

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    # Setup des deux consumers
    user_channel, user_connection = setup_consumer("user.sync", "api_orders_user", user_callback)
    product_channel, product_connection = setup_consumer("products.sync", "api_orders_product", product_callback)

    try:
        print("[*] En écoute sur user.sync et products.sync. Ctrl+C pour arrêter.")

        # On lance les deux canaux sur des threads différents (nécessaire car start_consuming est bloquant)
        import threading

        threading.Thread(target=user_channel.start_consuming).start()
        threading.Thread(target=product_channel.start_consuming).start()

    except KeyboardInterrupt:
        print("Arrêt des consumers.")
        user_channel.stop_consuming()
        product_channel.stop_consuming()
        user_connection.close()
        product_connection.close()
