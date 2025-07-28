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
    top: Optional[str]  
    available: Optional[str]  
    category: Optional[str]
    stock: Optional[str] 
    quantity: Optional[int]
    product_id: Optional[str]
