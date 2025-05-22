from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderDetails(BaseModel):
    price: float
    description: str
    color: str

class OrderCreate(BaseModel):
    product_name: str
    details: OrderDetails
    stock: int
    order_id: int
    customer_id: int

class OrderGet(OrderCreate):
    id: int
    created_at: Optional[datetime]
