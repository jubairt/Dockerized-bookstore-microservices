from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.auth import verify_token
import requests
import os
from dotenv import load_dotenv
load_dotenv()
router = APIRouter(prefix="/orders", tags=["Orders"])

BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://book_service:8002/books")
print("📘 Using BOOK_SERVICE_URL:", BOOK_SERVICE_URL)

@router.post("/", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), token_data: dict = Depends(verify_token)):
    username = token_data["payload"]["sub"]
    token = token_data["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Fetch book details
    response = requests.get(f"{BOOK_SERVICE_URL}/{order.book_id}", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = response.json()
    price = book_data["price"]
    book_name = book_data["title"]
    available_qty = book_data["quantity"]

    # 2. Check stock
    if available_qty < order.quantity:
        raise HTTPException(status_code=400, detail="Book out of stock")

    # 3. Reduce stock in Book Service
    reduce_response = requests.patch(
        f"{BOOK_SERVICE_URL}/{order.book_id}/reduce_stock",
        params={"quantity": order.quantity},
        headers=headers
    )

    if reduce_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to update stock")

    # 4. Create the order
    total_price = price * order.quantity

    new_order = models.Order(
        username=username,
        book_id=order.book_id,
        book_name=book_name,
        price=price,
        quantity=order.quantity,
        total_price=total_price
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order



@router.get("/", response_model=list[schemas.OrderResponse])
def get_my_orders(db: Session = Depends(get_db), token_data: dict = Depends(verify_token)):
    username = token_data["payload"]["sub"]
    return db.query(models.Order).filter(models.Order.username == username).all()
