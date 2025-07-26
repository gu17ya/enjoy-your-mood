from ..models.order import OrderIn, OrderOut
import uuid

class OrderService:
    def create(self, order: OrderIn) -> OrderOut:
        order_id = str(uuid.uuid4())
        # Здесь в будущем будет сохранение в Airtable
        return OrderOut(id=order_id)

def get_order_service() -> OrderService:
    return OrderService()