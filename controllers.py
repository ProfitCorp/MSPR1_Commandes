from sqlalchemy.orm import Session
from models import OrderDB
from schemas import OrderCreate, OrderGet, OrderDetails

# Récupérer toutes les commandes (chaque ligne = 1 produit dans une commande)
def get_all_orders(db: Session):
    orders = db.query(OrderDB).all()
    return [itemdb_to_order(item) for item in orders]

# Créer une ligne de commande
def create_order(db: Session, order_data: OrderCreate):
    db_order = OrderDB(
        product_name=order_data.product_name,
        price=order_data.details.price,
        description=order_data.details.description,
        color=order_data.details.color,
        stock=order_data.stock,
        order_id=order_data.order_id,
        customer_id=order_data.customer_id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return itemdb_to_order(db_order)

# Mettre à jour une ligne de commande
def update_order(db: Session, item_id: int, order_data: OrderCreate):
    db_order = db.query(OrderDB).filter(OrderDB.id == item_id).first()
    if not db_order:
        return None
    db_order.product_name = order_data.product_name
    db_order.price = order_data.details.price
    db_order.description = order_data.details.description
    db_order.color = order_data.details.color
    db_order.stock = order_data.stock
    db_order.order_id = order_data.order_id
    db_order.customer_id = order_data.customer_id
    db.commit()
    db.refresh(db_order)
    return db_order

# Supprimer une ligne de commande
def delete_order(db: Session, item_id: int):
    db_order = db.query(OrderDB).filter(OrderDB.id == item_id).first()
    if not db_order:
        return None
    db.delete(db_order)
    db.commit()
    return db_order

# Convertir un ItemDB vers un schéma de réponse OrderGet
def itemdb_to_order(item: OrderDB) -> OrderGet:
    return OrderGet(
        id=item.id,
        order_id=item.order_id,
        customer_id=item.customer_id,
        product_name=item.product_name,
        stock=item.stock,
        created_at=item.created_at,
        details=OrderDetails(
            price=item.price,
            description=item.description,
            color=item.color
        )
    )
