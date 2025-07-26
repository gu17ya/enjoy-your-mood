import os
from backend.airtable.airtable_client import AirtableClient
from dotenv import load_dotenv

load_dotenv()

def test_fetch_products():
    client = AirtableClient()
    products = client.fetch_products()
    print(f"Найдено товаров: {len(products)}")
    for p in products:
        print(f"{p['id']}: {p['name']} - Цена: {p['price']}")

if __name__ == "__main__":
    test_fetch_products()
