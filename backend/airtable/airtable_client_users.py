# backend/airtable/airtable_client_users.py

import os
import requests
from dotenv import load_dotenv
from utils.security import hash_password

load_dotenv()

class AirtableUserClient:
    def __init__(self):
        self.pat = os.getenv("AIRTABLE_PAT")
        self.base_id = os.getenv("AIRTABLE_BASE_ID")
        self.table_name = os.getenv("AIRTABLE_USERS_TABLE", "Users")
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        self.headers = {
            "Authorization": f"Bearer {self.pat}",
            "Content-Type": "application/json"
        }

    def get_user_by_email(self, email: str):
        url = f"{self.base_url}?filterByFormula=LOWER(Email)='{email.lower()}'"
        response = requests.get(url, headers=self.headers)
        records = response.json().get("records", [])
        return records[0] if records else None
    

    def get_user_by_id(self, user_id: str):
        url = f"{self.base_url}/{user_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None
    

    def create_user(self, name: str, email: str, phone: str, password: str):
        hashed = hash_password(password)
        data = {
            "fields": {
                "Name": name,
                "Email": email,
                "Phone": phone,
                "Password": hashed
            }
        }
        response = requests.post(self.base_url, json=data, headers=self.headers)
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Airtable create user error: {response.text}")