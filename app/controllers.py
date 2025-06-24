"""
Contient la logique métier pour gérer les commandes et produits dans la base de données.
"""
from mq.publish import publish_order_update, publish_order_delete,publish_order_create
from sqlalchemy.orm import Session
from models import OrderDB, ProductDB
from schemas import OrderCreate, OrderGet, ProductGet, ProductDetails, CustomerAddress, CustomerGet


def create_order(db: Session, order_data: OrderCreate):
    """Crée une commande avec ses produits dans la base de données."""
    order = OrderDB(customer_id=order_data.customer_id)
    db.add(order)
    db.commit()
    db.refresh(order)

    for product_id in order_data.products:
        product_db = db.query(ProductDB).get(product_id)
        if product_db:
            order.products.append(product_db)
        

    db.commit()
    publish_order_create(order_data.dict())
    return get_order_with_products(db, order.id)


def get_order_with_products(db: Session, order_id: int):
    """Retourne une commande complète avec ses produits liés."""
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        return None
    
    customer = order.customer
    customer_get = CustomerGet(
        id=customer.id,
        username=customer.username,
        first_name=customer.firstname,
        last_name=customer.lastname,
        company_name=customer.company_name,
        address=CustomerAddress(
            street_number=customer.street_number,
            street=customer.street,
            postal_code=customer.postalcode,
            city=customer.city
        )
    )

    return OrderGet(
        id=order.id,
        customer=customer_get,
        #created_at=order.created_at,
        products=[
            ProductGet(
                id=p.id,
                name=p.name,
                stock=p.stock,
                #created_at=p.created_at,
                details=ProductDetails(
                    price=p.price,
                    description=p.description,
                    color=p.color
                )
            )
            for p in order.products  # Utilisation directe de la relation
        ]
    )


def get_all_orders(db: Session):
    """Retourne toutes les commandes avec leurs produits."""
    orders = db.query(OrderDB).all()
    return [get_order_with_products(db, order.id) for order in orders]


def update_order(db: Session, order_id: int, order_data: OrderCreate):
    """Met à jour une commande et remplace ses produits liés."""
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        return None

    # Supprimer les associations existantes
    order.products = []

    # Associer les nouveaux produits
    products = db.query(ProductDB).filter(ProductDB.id.in_(order_data.products)).all()
    order.products = products

    # Mettre à jour le client
    order.customer_id = order_data.customer_id

    db.commit()
    db.refresh(order)

    publish_order_update(order_id, order_data.dict())
    return get_order_with_products(db, order_id)


def delete_order(db: Session, order_id: int):
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        return {"error": "Commande non trouvée"}

    # Supprimer les liens dans la table d'association
    order.products = []

    # Supprimer la commande
    db.delete(order)
    db.commit()

    publish_order_delete(order_id)
    return {"message": f"Commande {order_id} supprimée"}
