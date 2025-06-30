"""
Définit les 4 routes principales FastAPI pour gérer les commandes via API.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers import create_order, get_all_orders, update_order, delete_order
from schemas import OrderCreate, OrderGet, LoginInput
from auth.auth import create_access_token, authenticate_user
from auth.security import JWTBearer

router = APIRouter()


@router.post("/orders/", dependencies=[Depends(JWTBearer())], response_model=OrderGet)
def add_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle commande avec plusieurs produits."""
    return create_order(db, order)


@router.get("/orders/", dependencies=[Depends(JWTBearer())], response_model=list[OrderGet])
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

@router.post("/token")
def login_user(user: LoginInput):
    user = authenticate_user(user.username, user.password)
    if not user:
        raise HTTPException(status_code=401)

    token = create_access_token({
        "user": user.username,
        "role": user.role
        })
    return {"access_token": token, "token_type": "bearer"}
