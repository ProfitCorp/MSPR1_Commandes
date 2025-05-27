"""
Définit les 4 routes principales FastAPI pour gérer les commandes via API.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from controllers import create_order, get_all_orders, update_order, delete_order
from schemas import OrderCreate, OrderGet

router = APIRouter()


@router.post("/orders/", response_model=OrderGet)
def add_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle commande avec plusieurs produits."""
    return create_order(db, order)


@router.get("/orders/", response_model=list[OrderGet])
def get_orders(db: Session = Depends(get_db)):
    """Récupérer toutes les commandes avec leurs produits."""
    return get_all_orders(db)


@router.put("/orders/{order_id}", response_model=OrderGet)
def modify_order(order_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    """Mettre à jour une commande (et ses produits)."""
    return update_order(db, order_id, order)


@router.delete("/orders/{order_id}")
def remove_order(order_id: int, db: Session = Depends(get_db)):
    """Supprimer une commande ainsi que tous ses produits."""
    return delete_order(db, order_id)
