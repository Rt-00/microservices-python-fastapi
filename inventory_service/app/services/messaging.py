import json
import aio_pika

from ..models.product import Product
from ..database import SessionLocal
from ..config import settings


class MessagingService:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        """Conectar ao RabbitMQ"""
        self.connection = await aio_pika.connect_robust(settings.rabbitmq_url)
        self.channel = await self.connection.channel()

        # Declarar exchange
        await self.channel.declare_exchange(
            "orders", aio_pika.ExchangeType.TOPIC, durable=True
        )

        # Consumer para verificação de estoque
        queue = await self.channel.declare_queue("inventory_checks", durable=True)
        await queue.bind("orders", routing_key="inventory.check")
        await queue.consume(self.process_inventory_check)

        print("Connected to RabbitMQ and listening for inventory checks")

    async def disconnect(self):
        """Desconectar do RabbitMQ"""
        if self.connection:
            await self.connection.close()

    async def publish(self, routing_key: str, message: dict):
        """Publicar mensagem no RabbitMQ"""
        if not self.channel:
            raise Exception("RabbitMQ not connected")

        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
        )

    async def process_inventory_check(self, message: aio_pika.IncomingMessage):
        """Processar verificação de estoque"""
        async with message.process():
            data = json.loads(message.body.decode())
            order_id = data.get("order_id")
            product_id = data.get("product_id")
            quantity = data.get("quantity")

            db = SessionLocal()
            success = False

            try:
                product = db.query(Product).filter(Product.id == product_id).first()

                if product and product.stock >= quantity:
                    # Reservar estoque
                    product.stock -= quantity

                    db.commit()
                    success = True

                    print(f"Reserved {quantity} units of product {product_id}")
                else:
                    available = product.stock if product else 0
                    print(
                        f"Insufficient stock for product {product_id} (requested: {quantity}, available: {available})"
                    )

                # Responder ao Orders Service
                await self.publish(
                    "order_responses",
                    {
                        "order_id": order_id,
                        "product_id": product_id,
                        "success": success,
                    },
                )
            finally:
                db.close()


messaging_service = MessagingService()
