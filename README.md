# Microserviços com FastAPI e RabbitMQ

Sistema completo de microserviços com comunicação assíncrona via mensageria, onde cada serviço possui seu próprio banco de dados e responsabilidades bem definidas.

## Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Testando o Sistema](#-testando-o-sistema)
- [Monitoramento](#-monitoramento)
- [Troubleshooting](#-troubleshooting)
- [Desenvolvimento](#-desenvolvimento)

## Visão Geral

Este projeto implementa uma arquitetura de microserviços para um sistema de pedidos e-commerce, demonstrando:

- ✅ **Separação de responsabilidades** - Cada serviço tem uma função específica
- ✅ **Comunicação assíncrona** - Via RabbitMQ com pattern Pub/Sub
- ✅ **Bancos de dados isolados** - Cada serviço gerencia seus próprios dados
- ✅ **Event-driven architecture** - Serviços reagem a eventos do sistema
- ✅ **Containerização** - Tudo roda em Docker para fácil deploy
- ✅ **APIs REST** - Documentação automática com Swagger

### Serviços Implementados

1. **Orders Service**
   - Gerencia pedidos de clientes
   - PostgreSQL para persistência
   - Publica eventos de criação de pedidos

2. **Inventory Service**
   - Controla estoque de produtos
   - PostgreSQL para persistência
   - Valida e reserva itens automaticamente

3. **Notifications Service**
   - Registra todas as notificações do sistema
   - MongoDB para armazenamento flexível
   - Consome eventos de pedidos e inventário

## Arquitetura

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Orders Service │      │  RabbitMQ        │      │ Inventory       │
│  (PostgreSQL)   │─────▶│  Exchange Topic  │─────▶│ Service         │
│  Port: 8001     │◀─────│  orders_exchange │◀─────│ (PostgreSQL)    │
└─────────────────┘      └──────────────────┘      │ Port: 8002      │
                                  │                └─────────────────┘
                                  │
                                  ▼
                         ┌────────────────┐
                         │ Notifications  │
                         │ Service        │
                         │ (MongoDB)      │
                         │ Port: 8003     │
                         └────────────────┘
```

### Fluxo de Eventos

```
1. Cliente cria pedido
   └─▶ Orders Service salva no PostgreSQL (status: pending)
       └─▶ Publica evento: "inventory.check"

2. Inventory Service recebe evento
   └─▶ Verifica estoque disponível
       ├─▶ Se OK: Subtrai quantidade do estoque
       │   └─▶ Publica: "inventory.response" (success: true)
       └─▶ Se não: Publica: "inventory.response" (success: false)

3. Orders Service recebe resposta
   └─▶ Atualiza status do pedido (confirmed/cancelled)
       └─▶ Publica: "notifications.order"

4. Notifications Service recebe evento
   └─▶ Salva notificação no MongoDB
```

## Tecnologias

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.14 | Linguagem base |
| FastAPI | 0.128.0 | Framework web |
| PostgreSQL | 15 | Banco relacional |
| MongoDB | 7 | Banco NoSQL |
| RabbitMQ | 3 | Message broker |
| Docker | Latest | Containerização |
| SQLAlchemy | 2.0.45 | ORM |
| Pydantic | 2.12.5 | Validação de dados |
| aio-pika | 9.5.8 | Cliente RabbitMQ async |

## Estrutura do Projeto

```
microservices/
├── docker-compose.yml          # Orquestração de containers
├── .gitignore                  # Arquivos ignorados pelo Git
├── README.md                   # Este arquivo
├── orders-service/
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── config.py          # Configurações
│   │   ├── database.py        # Conexão PostgreSQL
│   │   ├── models/
│   │   │   └── order.py       # Model SQLAlchemy
│   │   ├── schemas/
│   │   │   └── order.py       # Schemas Pydantic
│   │   ├── routers/
│   │   │   └── orders.py      # Endpoints REST
│   │   └── services/
│   │       └── messaging.py   # Lógica RabbitMQ
│   ├── Dockerfile
│   └── requirements.txt
│
├── inventory-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── db/
│   │   │   └── base.py
│   │   ├── models/
│   │   │   └── product.py
│   │   ├── schemas/
│   │   │   └── product.py
│   │   ├── routers/
│   │   │   └── products.py
│   │   └── services/
│   │       └── messaging.py
│   ├── Dockerfile
│   └── requirements.txt
│
└── notifications-service/
    ├── app/
    │   ├── main.py
    │   ├── config.py
    │   ├── database.py
    │   ├── schemas/
    │   │   └── notification.py
    │   ├── routers/
    │   │   └── notifications.py
    │   └── services/
    │       └── messaging.py
    ├── Dockerfile
    └── requirements.txt
```

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/Rt-00/microservices-python-fastapi.git
cd microservices-python-fastapi
```

### 2. Inicie os serviços

```bash
docker-compose up -d --build
```

### 3. Verifique o status

```bash
docker-compose ps
```

Todos os containers devem estar com status `Up` ou `Up (healthy)`.

## Como Usar

### Acessar as APIs

Cada serviço tem sua própria documentação interativa (Swagger UI):

- **Orders Service**: http://localhost:8001/docs
- **Inventory Service**: http://localhost:8002/docs
- **Notifications Service**: http://localhost:8003/docs
- **RabbitMQ Management**: http://localhost:15672 (admin/admin)

### Exemplos de Requisições

#### 1. Listar produtos disponíveis

```bash
curl http://localhost:8002/products
```

**Resposta:**
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "stock": 10
  },
  {
    "id": 2,
    "name": "Mouse",
    "stock": 50
  },
  {
    "id": 3,
    "name": "Keyboard",
    "stock": 30
  }
]
```

#### 2. Criar um pedido

```bash
curl -X POST http://localhost:8001/orders \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2,
    "unit_price": 1500.00
  }'
```

**Resposta:**
```json
{
  "id": 1,
  "product_id": 1,
  "quantity": 2,
  "total_price": 3000.0,
  "status": "pending",
  "created_at": "2024-01-12T10:30:00"
}
```

#### 3. Verificar status do pedido

```bash
curl http://localhost:8001/orders/1
```

**Resposta (após processamento):**
```json
{
  "id": 1,
  "product_id": 1,
  "quantity": 2,
  "total_price": 3000.0,
  "status": "confirmed",
  "created_at": "2024-01-12T10:30:00"
}
```

#### 4. Verificar estoque atualizado

```bash
curl http://localhost:8002/products/1
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Laptop",
  "stock": 8
}
```

#### 5. Ver notificações

```bash
curl http://localhost:8003/notifications
```

**Resposta:**
```json
[
  {
    "id": "65a1b2c3d4e5f6g7h8i9j0k1",
    "order_id": 1,
    "status": "confirmed",
    "message": "Order 1 has been confirmed",
    "created_at": "2024-01-12T10:30:05"
  }
]
```

#### 6. Atualizar estoque manualmente

```bash
curl -X PATCH http://localhost:8002/products/1/stock \
  -H "Content-Type: application/json" \
  -d '{"stock": 20}'
```

## Monitoramento

### Logs dos Serviços

```bash
# Ver todos os logs
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f orders_service
docker-compose logs -f inventory_service
docker-compose logs -f notifications_service

# Ver últimas 50 linhas
docker-compose logs --tail=50 orders_service
```

### RabbitMQ Management UI

Acesse: http://localhost:15672
- **Usuário:** admin
- **Senha:** admin

**O que monitorar:**
- **Exchanges**: `orders_exchange` deve existir (tipo TOPIC)
- **Queues**: Verifique mensagens processadas
  - `inventory_checks`
  - `order_responses`
  - `notifications`
- **Connections**: 3 conexões ativas (uma por serviço)

##  Recursos Adicionais

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)
- [Docker Compose](https://docs.docker.com/compose/)
- [Pydantic](https://docs.pydantic.dev/)

## Próximos Passos

- [ ] Implementar testes unitários (pytest)
- [ ] Adicionar API Gateway (Kong/Traefik)
- [ ] Implementar autenticação JWT
- [ ] Circuit Breaker pattern
- [ ] Distributed tracing (Jaeger)
- [ ] Migrations com Alembic
- [ ] Logs estruturados (JSON)
- [ ] Métricas (Prometheus + Grafana)
- [ ] Dead Letter Queue
- [ ] Saga pattern para transações distribuídas
