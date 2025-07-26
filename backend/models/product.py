from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: str
    name: str
    description: Optional[str]
    price: float
    discount: Optional[float] = 0
    final_price: float
    photo_url: Optional[str]
    top: Optional[str]  # у тебя было "yes" или нет — лучше Optional[str]
    available: Optional[str]  # статус из Airtable (Visible, Not published и т.п.)
    category: Optional[str]
    stock: Optional[str]  # поле Stock с состоянием (Available, To order и т.п.)
    quantity: Optional[int]
    product_id: Optional[str]  # поле "Id" из Airtable
