"""
Point d'entrée principal de l'application FastAPI.

Ce module initialise l'application, crée les tables dans la base de données
et inclut les routes de l'API.
"""

from fastapi import FastAPI
from database import Base, engine
import routes as routes
from init import init_admin_user
from threading import Thread
from mq.receive import receive_product_message, receive_user_message

# Création des tables dans la base de données (si elles n'existent pas)
Base.metadata.create_all(bind=engine)

init_admin_user()

# Initialisation de l'application FastAPI
app = FastAPI()

# Inclusion des routes définies dans le module routes
app.include_router(routes.router)

@app.on_event("startup")
def _start_listener():
    """Launch the RabbitMQ listener in a background thread."""
    Thread(target=receive_user_message, daemon=True).start()
    Thread(target=receive_product_message, daemon=True).start()
