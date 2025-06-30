"""
Définit les schémas Pydantic pour valider les données d'entrée et de sortie de l'API.
"""

from typing import List
from datetime import datetime
from pydantic import BaseModel

class CustomerAddress(BaseModel):
    street_number: str
    street: str
    postal_code: str
    city: str

class CustomerGet(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    address: CustomerAddress
    company_name: str

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


class OrderCreate(BaseModel):
    """Commande à créer, avec le client et les produits associés."""

    customer_id: int
    products: List[int]


class OrderGet(BaseModel):
    """Commande complète retournée dans une réponse API."""

    id: int
    customer: CustomerGet
    products: List[ProductGet]

class LoginInput(BaseModel):
    username: str
    password: str

