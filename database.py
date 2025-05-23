"""
Ce module configure la base de données et fournit une session pour les requêtes SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion à la base de données SQLite
DATABASE_URL = "sqlite:///./orders.db"

# Création du moteur de base de données
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Création de la session locale (SessionLocal) à utiliser dans les dépendances FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles SQLAlchemy
Base = declarative_base()


def get_db():
    """
    Fournit une session de base de données pour la durée d'une requête.

    Cette fonction est utilisée comme dépendance dans FastAPI.
    Elle s'assure que la session est bien fermée après usage.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
