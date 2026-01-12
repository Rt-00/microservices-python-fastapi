from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from ..database import get_db
from ..models.product import Product
from ..schemas.product import ProductCreate, ProductResponse, ProductUpdate


router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Criar novo produto"""
    new_product = Product(name=product.name, stock=product.stock)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Buscar produto por ID"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.get("", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    """Listar todos os produtos"""
    return db.query(Product).all()


@router.patch("/{product_id}/stock", response_model=ProductResponse)
def update_stock(product_id: int, update: ProductUpdate, db: Session = Depends(get_db)):
    """Atualizar estoque de um produto"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.stock = update.stock

    db.commit()
    db.refresh(product)

    return product
