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
from logs.logger import setup_logger

Base.metadata.create_all(bind=engine)

init_admin_user()

app = FastAPI()

app.include_router(routes.router)

logger = setup_logger()

@app.on_event("startup")
def _start_listener():
    """Launch the RabbitMQ listener in a background thread."""
    Thread(target=receive_user_message, daemon=True).start()
    Thread(target=receive_product_message, daemon=True).start()
    logger.info("Application start")

