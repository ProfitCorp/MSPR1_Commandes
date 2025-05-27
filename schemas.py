"""
Définit les schémas Pydantic pour valider les données d'entrée et de sortie de l'API.
"""

from typing import List
from datetime import datetime
from pydantic import BaseModel


class ProductDetails(BaseModel):
    """Détails d'un produit (prix, description, couleur)."""

    price: float
    description: str
    color: str


class ProductCreate(BaseModel):
    """Données pour créer un produit dans une commande."""

    name: str
    stock: int
    details: ProductDetails


class ProductGet(ProductCreate):
    """Produit retourné dans une réponse, avec infos complètes."""

    id: int
    created_at: datetime
    order_id: int


class OrderCreate(BaseModel):
    """Commande à créer, avec le client et les produits associés."""

    customer_id: int
    products: List[ProductCreate]


class OrderGet(BaseModel):
    """Commande complète retournée dans une réponse API."""

    id: int
    customer_id: int
    created_at: datetime
    products: List[ProductGet]
