from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    book_id = Column(Integer)
    book_name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    total_price = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
