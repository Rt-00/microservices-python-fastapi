from datetime import datetime
from pydantic import BaseModel, Field


class NotificationResponse(BaseModel):
    id: str = Field(alias="_id")
    order_id: int
    status: str
    message: str
    created_at: datetime

    class Config:
        populate_by_name = True
