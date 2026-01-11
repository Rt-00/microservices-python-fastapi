from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..models.order import Order
from ..database import get_db
from ..schemas.order import OrderResponse


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=List[OrderResponse])
async def list_orders(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    """Listar todos os pedidos"""
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders
