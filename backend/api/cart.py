from fastapi import APIRouter, Request, Response, Form
from fastapi.responses import RedirectResponse
import json

router = APIRouter()

@router.post("/add-to-cart")
async def add_to_cart(request: Request, response: Response,
                      product_id: str = Form(...),
                      quantity: int = Form(...)):

    cart = json.loads(request.cookies.get("cart", "{}"))
    cart[product_id] = cart.get(product_id, 0) + quantity

    response = RedirectResponse(url="/cart", status_code=303)
    response.set_cookie("cart", json.dumps(cart))
    return response