from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    book_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    username: str
    book_id: int
    book_name: str
    price: float
    quantity: int
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True
