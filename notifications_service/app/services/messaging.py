from datetime import datetime
import json
import aio_pika

from ..config import settings
from ..database import database


class MessagingService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        """Conectar ao RabbitMQ"""
        self.connection = await aio_pika.connect_robust(settings.rabbitmq_url)
        self.channel = await self.connection.channel()

        # Declarar exchange
        self.exchange = await self.channel.declare_exchange(
            "orders", aio_pika.ExchangeType.TOPIC, durable=True
        )

        # Consumer para notificações
        queue = await self.channel.declare_queue("notifications", durable=True)
        await queue.bind("orders", routing_key="notifications.#")
        await queue.consume(self.process_notifications)

        print("Connected to RabbitMQ and listening for notifications")

    async def disconnect(self):
        """Desconectar do RabbitMQ"""
        if self.connection:
            await self.connection.close()

    async def process_notifications(self, message: aio_pika.IncomingMessage):
        """Processar e armazenar notificações"""
        async with message.process():
            data = json.loads(message.body.decode())

            notification = {
                "order_id": data.get("order_id"),
                "status": data.get("status"),
                "message": data.get("message"),
                "created_at": datetime.now(),
            }

            db = database.client[settings.database_name]
            result = await db.notifications.insert_one(notification)

            print(
                f"Notification created: {notification['message']} (ID: {result.inserted_id})"
            )


messaging_service = MessagingService()
