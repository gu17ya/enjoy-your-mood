from pydantic import BaseModel
from typing import List

class OrderIn(BaseModel):
    name: str
    phone: str
    email: str
    products: List[str]

class OrderOut(BaseModel):
    id: str
    status: str = "created"
