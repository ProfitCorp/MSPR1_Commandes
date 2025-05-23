"""
Définit les modèles SQLAlchemy pour les commandes et les produits.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# pylint: disable=too-few-public-methods
class OrderDB(Base):
    """Modèle représentant une commande client."""

    __tablename__ = "Orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    products = relationship("ProductDB", back_populates="order", cascade="all, delete")

# pylint: disable=too-few-public-methods
class ProductDB(Base):
    """Modèle représentant un produit lié à une commande."""

    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("Orders.id"))
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    color = Column(String)
    stock = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    order = relationship("OrderDB", back_populates="products")
