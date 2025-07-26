from fastapi import FastAPI
from backend.api import products_router, orders_router, users_router, categories_router

app = FastAPI()

# Подключение роутеров
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(users_router)
app.include_router(categories_router)