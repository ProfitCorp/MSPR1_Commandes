import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models import CustomerDB, ProductDB
from auth.auth import create_access_token
from auth.security import hash_password

SQLALCHEMY_DATABASE_URL = "sqlite:///../test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    admin = CustomerDB(username="admin", password=hash_password("adminpass"), role="admin")
    user = CustomerDB(username="user", password=hash_password("userpass"), role="user")
    db.add_all([admin, user])
    db.commit()

    product1 = ProductDB(name="Laptop", stock=10, price=1000.0, description="Laptop puissant", color="Noir")
    product2 = ProductDB(name="Souris", stock=50, price=25.0, description="Souris ergonomique", color="Gris")
    db.add_all([product1, product2])
    db.commit()

    yield
    db.close()

def get_token(username, role, user_id):
    return create_access_token({"sub": username, "role": role, "user_id": user_id})

def auth_headers(username, role, user_id):
    token = get_token(username, role, user_id)
    return {"Authorization": f"Bearer {token}"}

def test_create_order_as_admin():
    headers = auth_headers("admin", "admin", 1)
    payload = {
        "customer_id": 1,
        "products": [1, 2]
    }
    response = client.post("/orders/", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["customer"]["username"] == "admin"
    assert len(data["products"]) == 2

def test_get_all_orders_as_admin():
    headers = auth_headers("admin", "admin", 1)
    client.post("/orders/", json={"customer_id": 1, "products": [1]}, headers=headers)
    response = client.get("/orders/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["products"][0]["name"] == "Laptop"

def test_get_orders_as_user_only_own():
    headers_admin = auth_headers("admin", "admin", 1)
    headers_user = auth_headers("user", "user", 2)

    client.post("/orders/", json={"customer_id": 1, "products": [1]}, headers=headers_admin)
    client.post("/orders/", json={"customer_id": 2, "products": [2]}, headers=headers_admin)

    response = client.get("/orders/", headers=headers_admin)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["customer"]["username"] == "user"

def test_update_order():
    headers = auth_headers("admin", "admin", 1)
    # Crée une commande
    res = client.post("/orders/", json={"customer_id": 1, "products": [1]}, headers=headers)
    order_id = res.json()["id"]

    update_payload = {
        "customer_id": 1,
        "products": [2]
    }
    response = client.put(f"/orders/{order_id}", json=update_payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 1
    assert data["products"][0]["name"] == "Souris"

def test_delete_order():
    headers = auth_headers("admin", "admin", 1)
    res = client.post("/orders/", json={"customer_id": 1, "products": [1]}, headers=headers)
    order_id = res.json()["id"]

    response = client.delete(f"/orders/{order_id}", headers=headers)
    assert response.status_code == 200
    assert "supprimée" in response.json()["message"]

    get_response = client.get("/orders/", headers=headers)
    assert len(get_response.json()) == 0
