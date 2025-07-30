from backend.models.product import Product
from ..airtable.airtable_client_products import AirtableClient

class ProductService:
    def __init__(self, airtable_client: AirtableClient):
        self.airtable = airtable_client

    def get_all(self) -> list[Product]:
        data = self.airtable.fetch_products()
        return [Product(**item) for item in data]

def get_product_service() -> ProductService:
    client = AirtableClient()
    return ProductService(client)