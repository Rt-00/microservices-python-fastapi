from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    stock: int


class ProductResponse(BaseModel):
    id: int
    name: str
    stock: int

    class Config:
        from_attributes = True
