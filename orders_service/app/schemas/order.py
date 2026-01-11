from pydantic import BaseModel
from datetime import datetime


class OrderCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
