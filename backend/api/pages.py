from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.airtable.airtable_client import AirtableClient
from datetime import datetime
import os

router = APIRouter()
client = AirtableClient()

# Путь до frontend/templates
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
