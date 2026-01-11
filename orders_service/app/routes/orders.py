from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..models.order import Order
from ..database import get_db
from ..schemas.order import OrderCreate, OrderResponse


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Criar novo pedido"""
    total = order.quantity * order.unit_price

    new_order = Order(
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total,
        status="pending",
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("", response_model=List[OrderResponse])
async def list_orders(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    """Listar todos os pedidos"""
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders
