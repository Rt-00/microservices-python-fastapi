from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from ..database import get_db
from ..models.product import Product
from ..schemas.product import ProductResponse


router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    """Listar todos os produtos"""
    return db.query(Product).all()
