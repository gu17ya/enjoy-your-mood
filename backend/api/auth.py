from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from backend.services.user_service import UserService

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

service = UserService()

# Страница логина (GET)
@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

# Логин (POST)
@router.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = service.authenticate_user(email, password)
    if not user:
        return templates.TemplateResponse("auth/login.html", {
            "request": request,
            "error": "Неверный логин или пароль"
        })

    request.session["user_id"] = user["id"]
    response = RedirectResponse(url=f"/{user['id']}/dashboard", status_code=status.HTTP_302_FOUND)
    return response

# Страница регистрации (GET)
@router.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

# Регистрация (POST)
@router.post("/register")
async def register_post(
    request: Request,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        service.register_user(email=email, password=password, name=name, phone=phone)
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    except ValueError as e:
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": str(e)
        })
