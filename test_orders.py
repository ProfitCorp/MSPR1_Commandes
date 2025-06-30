"""
Tests des principales routes de l'API Orders :
- POST /orders/
- GET /orders/
- PUT /orders/{order_id}
- DELETE /orders/{order_id}

Utilise une base SQLite temporaire pour isoler les tests.
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Base de données de test
TEST_DB_FILE = "./test_orders.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """
    Initialise une base SQLite temporaire pour les tests, puis la supprime à la fin.
    """
    Base.metadata.create_all(bind=engine)
    yield
    if os.path.exists(TEST_DB_FILE):
        engine.dispose()
        os.remove(TEST_DB_FILE)


def override_get_db():
    """
    Surcharge la dépendance de base de données pour pointer vers la base de test.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_post_order():
    """
    Vérifie que l'API permet de créer une commande avec un produit (POST /orders/).
    """
    payload = {
        "customer_id": 7,
        "products": [
            {
                "name": "Produit A",
                "stock": 10,
                "details": {"price": 99.99, "description": "desc A", "color": "red"},
            }
        ],
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 200
    assert response.json()["customer_id"] == 7


def test_get_orders():
    """
    Vérifie que l'API retourne la liste des commandes existantes (GET /orders/).
    """
    response = client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_put_order():
    """
    Vérifie que l'API permet de modifier une commande existante (PUT /orders/{id}).
    """
    payload = {
        "customer_id": 8,
        "products": [
            {
                "name": "Produit B",
                "stock": 5,
                "details": {"price": 49.99, "description": "desc B", "color": "blue"},
            }
        ],
    }
    response = client.put("/orders/1", json=payload)
    assert response.status_code == 200
    assert response.json()["customer_id"] == 8


def test_delete_order():
    """
    Vérifie que l'API supprime correctement une commande (DELETE /orders/{id}).
    """
    response = client.delete("/orders/1")
    assert response.status_code == 200
