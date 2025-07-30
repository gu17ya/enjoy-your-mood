# backend/services/order_service.py

from backend.airtable.airtable_client_orders import AirtableOrderClient
from backend.models.order import OrderIn, OrderOut

class OrderService:
    def __init__(self):
        self.client = AirtableOrderClient()

    def create(self, order: OrderIn) -> OrderOut:
        # Подготовка данных в формат Airtable
        data = {
            "UserId": order.user_id,
            "ProductId": order.product_id,
            "Quantity": order.quantity,
            "Status": order.status or "new",
            # добавьте другие поля, если нужно
        }
        record = self.client.create_order(data)
        # Возвращаем OrderOut с id записи Airtable
        return OrderOut(
            id=record["id"],
            user_id=order.user_id,
            product_id=order.product_id,
            quantity=order.quantity,
            status=order.status or "new",
        )

    def get_orders_by_user(self, user_id: str) -> list[OrderOut]:
        records = self.client.get_orders_by_user_id(user_id)
        orders = []
        for r in records:
            fields = r.get("fields", {})
            orders.append(OrderOut(
                id=r["id"],
                user_id=fields.get("UserId"),
                product_id=fields.get("ProductId"),
                quantity=fields.get("Quantity"),
                status=fields.get("Status")
            ))
        return orders


def get_order_service() -> OrderService:
    return OrderService()
