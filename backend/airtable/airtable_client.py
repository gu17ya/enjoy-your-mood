import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AirtableClient:
    def __init__(self):
        self.pat = os.getenv("AIRTABLE_PAT")
        self.base_id = os.getenv("AIRTABLE_BASE_ID")
        self.table_name = os.getenv("AIRTABLE_PRODUCTS_TABLE", "Products")
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        self.headers = {
            "Authorization": f"Bearer {self.pat}",
            "Content-Type": "application/json"
        }

    def fetch_products(self) -> list[dict]:
        resp = requests.get(self.base_url, headers=self.headers)
        records = resp.json().get("records", [])
        result = []
        for r in records:
            fields = r["fields"]
            result.append({
                "id": r["id"],  # id Airtable записи
                "name": fields.get("Name"),
                "description": fields.get("Description"),
                "price": fields.get("Price", 0),
                "discount": fields.get("Discount", 0),
                "final_price": fields.get("Final Price", 0),
                "photo_url": fields.get("Image", [{}])[0].get("url") if fields.get("Image") else None,
                "top": fields.get("Top") in ("yes", "true", True),
                "available": fields.get("Available"),
                "category": fields.get("Category"),
                "stock": fields.get("Stock"),
                "quantity": fields.get("Quantity"),
                "product_id": fields.get("Id"),  # твой кастомный ID из Airtable
            })
        return result
