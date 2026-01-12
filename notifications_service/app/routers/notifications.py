from typing import List
from fastapi import APIRouter, Depends

from ..database import get_database
from ..schemas.notification import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=List[NotificationResponse])
async def list_notifications(skip: int = 0, limit: int = 10, db=Depends(get_database)):
    """Listar notificações"""
    cursor = db.notifications.find().sort("created_at", -1).skip(skip).limit(limit)
    notifications = []

    async for doc in cursor:
        notifications.append(
            {
                "_id": str(doc["_id"]),
                "order_id": doc["order_id"],
                "status": doc["status"],
                "message": doc["message"],
                "created_at": doc["created_at"],
            }
        )

    return notifications


@router.get("/order/{order_id}", response_model=List[NotificationResponse])
async def get_order_notifications(order_id: int, db=Depends(get_database)):
    """Buscar notificações de um pedido específico"""
    cursor = db.notifications.find({"order_id": order_id}).sort("created_at", -1)
    notifications = []

    async for doc in cursor:
        notifications.append(
            {
                "_id": str(doc["_id"]),
                "order_id": doc["order_id"],
                "status": doc["status"],
                "message": doc["message"],
                "created_at": doc["created_at"],
            }
        )

    return notifications
