from models import CustomerDB, ProductDB
from auth.security import hash_password

def create_user(db, data):
    new_user = CustomerDB(
        username=data.get("username"),
        password=hash_password(data.get("password")),
        role=data.get("role", "user"),
        firstname=data.get("firstName"),
        lastname=data.get("lastName"),
        street_number=data["address"].get("streetNumber"),
        street=data["address"].get("street"),
        postalcode=data["address"].get("postalCode"),
        city=data["address"].get("city"),
        company_name=data.get("companyName")
    )
    db.add(new_user)
    db.commit()

def update_user(db, user_id, data):
    user = db.query(CustomerDB).filter(CustomerDB.id == user_id).first()
    if not user:
        return

    if "username" in data:
        user.username = data["username"]
    if "password" in data:
        user.password = hash_password(data["password"])
    if "role" in data:
        user.role = data["role"]
    if "firstName" in data:
        user.firstname = data["firstName"]
    if "lastName" in data:
        user.lastname = data["lastName"]
    if "address" in data:
        addr = data["address"]
        if "streetNumber" in addr:
            user.street_number = addr["streetNumber"]
        if "street" in addr:
            user.street = addr["street"]
        if "postalCode" in addr:
            user.postalcode = addr["postalCode"]
        if "city" in addr:
            user.city = addr["city"]
    if "companyName" in data:
        user.company_name = data["companyName"]

    db.commit()

def delete_user(db, user_id):
    user = db.query(CustomerDB).filter(CustomerDB.id == user_id).first()
    if not user:
        return

    db.delete(user)
    db.commit()

def create_product(db, product_id, data):
    new_product = ProductDB(
        id=product_id,
        name=data.get("name"),
        price=data["details"].get("price"),
        description=data["details"].get("description"),
        color=data["details"].get("color"),
        stock=data.get("stock")
    )
    db.add(new_product)
    db.commit()

def update_product(db, product_id, data):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        return

    if "name" in data:
        product.name = data["name"]
    if "details" in data:
        details = data["details"]
        if "price" in details:
            product.price = details["price"]
        if "description" in details:
            product.description = details["description"]
        if "color" in details:
            product.color = details["color"]
    if "stock" in data:
        product.stock = data["stock"]

    db.commit()

def delete_product(db, product_id):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        return

    db.delete(product)
    db.commit() 