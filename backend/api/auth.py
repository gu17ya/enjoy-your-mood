from fastapi import APIRouter, Request, Form, Depends, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.models.user_model import User
from database.db import get_db
from utils.security import hash_password, verify_password

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates") 

# Получить пользователя по email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Получить пользователя по телефону (если нужно)
def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()

# Страница логина (GET)
@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

# Логин (POST)
@router.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("auth/login.html", {
            "request": request,
            "error": "Неверный логин или пароль"
        })

    response = RedirectResponse(url=f"/{user.id}/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie("user_email", email)
    return response

# Страница регистрации (GET)
@router.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

# Регистрация (POST)
@router.post("/register")
async def register_post(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Проверяем уникальность email и телефона
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email уже занят")
    if get_user_by_phone(db, phone):
        raise HTTPException(status_code=400, detail="Телефон уже занят")

    hashed_pw = hash_password(password)
    new_user = User(
        name=name,
        phone=phone,
        email=email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
