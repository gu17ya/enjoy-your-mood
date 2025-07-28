from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from backend.api import products_router, orders_router, users_router, categories_router, pages, auth, account  
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")
templates = Jinja2Templates(directory="frontend/templates")

# Подключение роутеров
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(account.router)

# Подключение статики
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend", "static")), name="static")

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)

