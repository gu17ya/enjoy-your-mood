# backend/airtable/airtable_client_orders.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AirtableOrderClient:
    def __init__(self):
        self.pat = os.getenv("AIRTABLE_PAT")
        self.base_id = os.getenv("AIRTABLE_BASE_ID")
        self.table_name = os.getenv("AIRTABLE_ORDERS_TABLE", "Orders")
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        self.headers = {
            "Authorization": f"Bearer {self.pat}",
            "Content-Type": "application/json"
        }

    def create_order(self, user_email: str, items: list, total: float, status: str = "new"):
        data = {
            "fields": {
                "User Email": user_email,
                "Items": str(items),  # можно форматировать красиво
                "Total": total,
                "Status": status
            }
        }
        response = requests.post(self.base_url, headers=self.headers, json=data)
        return response.json()

    def fetch_orders_by_email(self, email: str):
        url = f"{self.base_url}?filterByFormula=LOWER({{User Email}})='{email.lower()}'"
        response = requests.get(url, headers=self.headers)
        return response.json().get("records", [])
