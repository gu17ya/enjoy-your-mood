
from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.services.user_service import UserService
from database.db import get_db
from datetime import datetime
from backend.models.user_model import User


now = datetime.now()
router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

# Общая функция получения пользователя
def get_user_or_404(user_id: int, db: Session):
    service = UserService(db)
    user = service.get_user_by_id(user_id)
    if not user:
        return None
    return user

@router.get("/{user_id}/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)
    if not user:
        return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404, )
    return templates.TemplateResponse("account/dashboard.html", {"request": request, "user": user, "now": now })

@router.get("/{user_id}/personal-information", response_class=HTMLResponse)
async def personal_information(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)
    if not user:
        return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("account/personal_information.html", {"request": request, "user": user, "now": now })

@router.post("/{user_id}/personal-information")
async def personal_info_post(
    request: Request,
    user_id: int,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    db: Session = Depends(get_db),
):
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    user.name = name
    user.email = email
    user.phone = phone

    db.commit()
    message = "Дані успішно оновлені"
    return templates.TemplateResponse(
        "account/personal_information.html",
        {"request": request, "user": user, "message": message, "now": now },
        status_code=status.HTTP_200_OK,
    )

@router.get("/{user_id}/orders", response_class=HTMLResponse)
async def orders(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)
    if not user:
        return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("account/orders.html", {"request": request, "user": user, "now": now })

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("user_email")
    return response