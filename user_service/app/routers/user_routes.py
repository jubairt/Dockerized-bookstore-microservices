from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.schemas import UserCreate, UserLogin, UserOut
from app.models import User
from app.database import get_db
from app.auth import create_token, verify_token
from app.logger import get_logger

router = APIRouter(prefix="/users", tags=["Users"])
logger = get_logger(__name__)

# Register
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.name == user.name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = bcrypt.hash(user.password[:72])
    new_user = User(name=user.name, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"New user registered: {user.name}")
    return new_user


# Login
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.name).first()
    if not db_user or not bcrypt.verify(user.password[:72], db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.name)
    logger.info(f"User logged in: {user.name}")
    return {"access_token": token}


# Authenticated endpoint (/me)
@router.get("/me", response_model=UserOut)
def get_me(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.name == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"Fetched profile for: {username}")
    return user
