import json
import aio_pika

from ..models.order import Order
from ..database import SessionLocal
from ..config import settings


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

        # Iniciar consumer
        queue = await self.channel.declare_queue("order_responses", durable=True)
        await queue.bind("orders", routing_key="inventory.response")
        await queue.consume(self.process_inventory_response)

        print("Connected to RabbitMQ")

    async def disconnect(self):
        """Desconectar do RabbitMQ"""
        if self.connection:
            await self.connection.close()

    async def publish(self, routing_key: str, message: dict):
        """Publicar mensagem no RabbitMQ"""
        if not self.channel:
            raise Exception("RabbitMQ not connected")

        await self.exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
        )

    async def process_inventory_response(self, message: aio_pika.IncomingMessage):
        """Processar resposta do Inventory Service"""
        data = json.loads(message.body.decode())
        order_id = data.get("order_id")
        success = data.get("success")

        db = SessionLocal()
        try:
            order = db.query(Order).filter(Order.id == order_id).first()

            if order:
                order.status = "confirmed" if success else "cancelled"
                db.commit()

                await self.publish(
                    "notifications.order",
                    {
                        "order_id": order_id,
                        "status": order.status,
                        "message": f"Order {order_id} has been {order.status}",
                    },
                )
        finally:
            db.close()


messaging_service = MessagingService()
