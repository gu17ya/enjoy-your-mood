from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..airtable.airtable_client_products import AirtableClient
from datetime import datetime
import os
import json

router = APIRouter()
client = AirtableClient()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend", "templates"))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    products = client.fetch_products()
    categories = sorted(set(p["category"] for p in products if p["category"]))
    return templates.TemplateResponse("home.html", {
        "request": request,
        "products": products,
        "categories": categories,
        "now": datetime.now()
    })

@router.get("/category/{category_name}", response_class=HTMLResponse)
async def category_page(request: Request, category_name: str):
    products = client.fetch_products()
    category_products = [p for p in products if p.get("category", "").lower() == category_name.lower()]
    if not category_products:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    return templates.TemplateResponse("category.html", {
        "request": request,
        "category_name": category_name,
        "products": category_products,
        "now": datetime.now()
    })

@router.get("/product/{product_name}", response_class=HTMLResponse)
async def product_page(request: Request, product_name: str):
    products = client.fetch_products()
    product_name = product_name.lower()

    product = next(
        (
            p for p in products
            if isinstance(p.get("name"), str) and p["name"].lower() == product_name
        ),
        None
    )

    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    return templates.TemplateResponse("product.html", {
        "request": request,
        "product": product,
        "now": datetime.now()
    })


@router.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request):
    cart_data = json.loads(request.cookies.get("cart", "{}"))
    products = client.fetch_products()
    cart_items = []

    for pid, qty in cart_data.items():
        product = next((p for p in products if str(p["id"]) == pid), None)
        if product:
            cart_items.append({
                "product": product,
                "quantity": qty,
                "subtotal": qty * float(product["final_price"])
            })

    total = sum(item["subtotal"] for item in cart_items)
    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart_items": cart_items,
        "total": total,
        "now": datetime.now()
    })