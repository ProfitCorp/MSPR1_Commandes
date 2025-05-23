"""
Contient la logique métier pour gérer les commandes et produits dans la base de données.
"""

from sqlalchemy.orm import Session
from models import OrderDB, ProductDB
from schemas import OrderCreate, OrderGet, ProductGet, ProductDetails


def create_order(db: Session, order_data: OrderCreate):
    """Crée une commande avec ses produits dans la base de données."""
    order = OrderDB(customer_id=order_data.customer_id)
    db.add(order)
    db.commit()
    db.refresh(order)

    for product in order_data.products:
        product_db = ProductDB(
            name=product.name,
            stock=product.stock,
            price=product.details.price,
            description=product.details.description,
            color=product.details.color,
            order_id=order.id,
        )
        db.add(product_db)

    db.commit()
    return get_order_with_products(db, order.id)


def get_order_with_products(db: Session, order_id: int):
    """Retourne une commande complète avec ses produits."""
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        return None

    products = db.query(ProductDB).filter(ProductDB.order_id == order.id).all()

    return OrderGet(
        id=order.id,
        customer_id=order.customer_id,
        created_at=order.created_at,
        products=[
            ProductGet(
                id=p.id,
                name=p.name,
                order_id=p.order_id,
                stock=p.stock,
                created_at=p.created_at,
                details=ProductDetails(
                    price=p.price, description=p.description, color=p.color
                ),
            )
            for p in products
        ],
    )


def get_all_orders(db: Session):
    """Retourne toutes les commandes avec leurs produits."""
    orders = db.query(OrderDB).all()
    return [get_order_with_products(db, order.id) for order in orders]


def update_order(db: Session, order_id: int, order_data: OrderCreate):
    """Met à jour une commande et remplace ses produits."""
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        return None

    db.query(ProductDB).filter(ProductDB.order_id == order_id).delete()

    for product in order_data.products:
        new_product = ProductDB(
            name=product.name,
            stock=product.stock,
            price=product.details.price,
            description=product.details.description,
            color=product.details.color,
            order_id=order_id,
        )
        db.add(new_product)

    order.customer_id = order_data.customer_id
    db.commit()
    db.refresh(order)

    return get_order_with_products(db, order_id)


def delete_order(db: Session, order_id: int):
    """Supprime une commande et tous ses produits associés."""
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        return {"error": "Commande non trouvée"}

    db.query(ProductDB).filter(ProductDB.order_id == order_id).delete()
    db.delete(order)
    db.commit()
    return {"message": f"Commande {order_id} et ses produits supprimés"}
