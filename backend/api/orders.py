from fastapi import APIRouter, Depends
from ..models.order import OrderIn, OrderOut
from ..services.order_service import OrderService, get_order_service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderOut)
def new_order(order: OrderIn, service: OrderService = Depends(get_order_service)):
    return service.create(order)