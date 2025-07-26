from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from ..services.product_service import ProductService, get_product_service

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_class=HTMLResponse)
def list_products(service: ProductService = Depends(get_product_service)):
    products = service.get_all()

    # Соберём простой HTML для вывода
    html_content = "<h1>Товары</h1><ul>"
    for p in products:
        html_content += f"<li>{p.name} - Цена: {p.final_price} - В наличии: {p.stock} - Кол-во: {getattr(p, 'quantity', 'N/A')}</li>"
    html_content += "</ul>"

    return html_content
