from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import get_all_orders, create_order, update_order, delete_order
from database import get_db
from schemas import OrderCreate, OrderGet

router = APIRouter()


@router.get("/orders/", response_model=list[OrderGet])
def get_orders(db: Session = Depends(get_db)):
    return get_all_orders(db)


@router.post("/orders/", response_model=OrderGet)
def add_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)


@router.put("/orders/{item_id}", response_model=OrderGet)
def modify_order(item_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    updated = update_order(db, item_id, order)
    if not updated:
        return {"error": "Commande non trouvée"}
    return updated


@router.delete("/orders/{item_id}")
def remove_order(item_id: int, db: Session = Depends(get_db)):
    deleted = delete_order(db, item_id)
    if not deleted:
        return {"error": "Commande non trouvée"}
    return {"message": f"Commande {item_id} supprimée"}
