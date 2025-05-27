"""
Point d'entrée principal de l'application FastAPI.

Ce module initialise l'application, crée les tables dans la base de données
et inclut les routes de l'API.
"""

from fastapi import FastAPI
from database import Base, engine
import routes

# Création des tables dans la base de données (si elles n'existent pas)
Base.metadata.create_all(bind=engine)

# Initialisation de l'application FastAPI
app = FastAPI()

# Inclusion des routes définies dans le module routes
app.include_router(routes.router)
