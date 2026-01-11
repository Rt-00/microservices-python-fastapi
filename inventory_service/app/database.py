from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings
from .db.base import Base

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from .models.product import Product  # importa TODOS os models

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    if db.query(Product).count() == 0:
        db.add_all(
            [
                Product(name="Laptop", stock=10),
                Product(name="Mouse", stock=50),
                Product(name="Keyboard", stock=30),
            ]
        )
        db.commit()

    db.close()
