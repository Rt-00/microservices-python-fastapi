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
