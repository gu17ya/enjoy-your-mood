from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.services.user_service import UserService
from datetime import datetime

now = datetime.now()
router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
service = UserService()

# Страница: Кабінет користувача
@router.get("/{user_id}/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user_id: str):
    user = service.get_user_by_id(user_id)
    if not user:
        return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("account/dashboard.html", {"request": request, "user": user, "now": now})

# Страница: Особисті дані (GET)
@router.get("/{user_id}/personal-information", response_class=HTMLResponse)
async def personal_information(request: Request, user_id: str):
    user = service.get_user_by_id(user_id)
    if not user:
        return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("account/personal_information.html", {"request": request, "user": user, "now": now})

# Обновление особистих даних (POST)
@router.post("/{user_id}/personal-information")
async def personal_info_post(
    request: Request,
    user_id: str,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None)
):
    try:
        updated_user = service.update_user(user_id=user_id, name=name, email=email, phone=phone)
        message = "Дані успішно оновлені"
        return templates.TemplateResponse(
            "account/personal_information.html",
            {"request": request, "user": updated_user, "message": message, "now": now},
            status_code=status.HTTP_200_OK,
        )
    except ValueError:
        return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)

# Страница: Замовлення
@router.get("/{user_id}/orders", response_class=HTMLResponse)
async def orders(request: Request, user_id: str):
    user = service.get_user_by_id(user_id)
    if not user:
        return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("account/orders.html", {"request": request, "user": user, "now": now})

# Вихід
@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    response = RedirectResponse(url="/")
    response.delete_cookie("user_email")
    return response
