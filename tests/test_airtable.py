import os
from backend.airtable.airtable_client_products import AirtableClient
from dotenv import load_dotenv

load_dotenv()

def test_fetch_products():
    client = AirtableClient()
    products = client.fetch_products()
    print(f"Найдено товаров: {len(products)}")
    for p in products:
        print(f"{p['id']}: {p['name']} Price {p['price']}, Discount {p['discount']}, Description {p['description']}, Top {p['top']}, available {p['available']}, Category {p['category']}")

if __name__ == "__main__":
    test_fetch_products()
    
# python -m tests.test_airtable