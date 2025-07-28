from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.session import SessionLocal 
from backend.services.user_service import UserService
from backend.models.user_model import User
from utils.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserIn(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

@router.post("/register", response_model=UserOut)
def register(user: UserIn, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        new_user = service.register_user(user.email, user.password)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user: UserIn, request: Request, db: Session = Depends(get_db)):
    service = UserService(db)
    auth_user = service.authenticate_user(user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    
    # Сохраняем в сессии user_id
    request.session["user_id"] = auth_user.id
    
    return auth_user
