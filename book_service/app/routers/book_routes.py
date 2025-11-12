from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.logger import get_logger
from app.auth import verify_token

router = APIRouter(prefix="/books", tags=["Books"])
logger = get_logger(__name__)


@router.get("/", response_model=list[schemas.BookResponse])
def list_books(db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    books = db.query(models.Book).all()
    return books

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.patch("/{book_id}/reduce_stock")
def reduce_stock(book_id: int, quantity: int, db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    
    book.quantity -= quantity
    db.commit()
    db.refresh(book)
    return {"message": f"Reduced {quantity} from stock. Remaining: {book.quantity}"}
