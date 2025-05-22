from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from database import Base
from datetime import datetime
from datetime import timezone 


class OrderDB(Base):
    __tablename__ = "Orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    order_id = Column(Integer, index=True)         
    customer_id = Column(Integer, index=True)      
    product_name = Column(String)                           
    price = Column(Float)                           
    description = Column(String)                    
    color = Column(String)                          
    stock = Column(Integer)                         
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))