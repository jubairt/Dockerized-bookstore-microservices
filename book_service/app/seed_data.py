import csv
from sqlalchemy.orm import Session
from app.models import Book
from app.database import SessionLocal

def seed_books():
    db: Session = SessionLocal()
    with open("app/data/books.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not db.query(Book).filter_by(title=row["title"]).first():
                book = Book(
                    title=row["title"],
                    author=row["author"],
                    price=float(row["price"]),
                    quantity=int(row["quantity"])
                )
                db.add(book)
        db.commit()
    db.close()
