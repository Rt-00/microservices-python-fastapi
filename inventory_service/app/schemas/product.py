from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    name: str
    stock: int

    class Config:
        from_attributes = True
