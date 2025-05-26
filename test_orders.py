import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Base de données de test
TEST_DB_FILE = "./test_orders.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    if os.path.exists(TEST_DB_FILE):
        engine.dispose()
        os.remove(TEST_DB_FILE)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_post_order():
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
    response = client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_put_order():
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
    response = client.delete("/orders/1")
    assert response.status_code == 200
