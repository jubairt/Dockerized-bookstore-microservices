# app/schemas.py

from pydantic import BaseModel

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float
    quantity: int

    class Config:
        from_attributes = True
