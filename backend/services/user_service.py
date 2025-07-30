from backend.airtable.airtable_client_users import AirtableUserClient
from utils.security import verify_password

class UserService:
    def __init__(self):
        self.airtable = AirtableUserClient()

    def register_user(self, name: str, email: str, phone: str, password: str):
        existing_user = self.airtable.get_user_by_email(email)
        if existing_user:
            raise ValueError("Пользователь уже существует")

        return self.airtable.create_user(name, email, phone, password)

    def authenticate_user(self, email: str, password: str):
        record = self.airtable.get_user_by_email(email)
        if not record:
            return None

        user = record["fields"]
        stored_hashed_password = user.get("Password")
        if not verify_password(password, stored_hashed_password):
            return None

        return {
            "id": record["id"],
            "name": user.get("Name"),
            "email": user.get("Email"),
            "phone": user.get("Phone")
        }
    
    def get_user_by_id(self, user_id: str):
        record = self.airtable.get_user_by_id(user_id)
        if not record:
            return None

        user = record["fields"]
        return {
            "id": record["id"],
            "name": user.get("Name"),
            "email": user.get("Email"),
            "phone": user.get("Phone")
        }