from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.api import products_router, orders_router, users_router, categories_router, pages
import os

app = FastAPI()

# Подключение роутеров
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(pages.router)  

# Подключение статики
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend", "static")), name="static")