from sqlalchemy.orm import Session
from backend.models.user_model import User
from utils.security import hash_password, verify_password
from sqlalchemy.exc import SQLAlchemyError

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, email: str, password: str):
        existing = self.db.query(User).filter_by(email=email).first()
        if existing:
            raise ValueError("Пользователь уже существует")

        hashed = hash_password(password)
        new_user = User(email=email, hashed_password=hashed)
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except SQLAlchemyError:
            self.db.rollback()
            raise RuntimeError("Ошибка при сохранении пользователя")

    def authenticate_user(self, email: str, password: str):
        user = self.db.query(User).filter_by(email=email).first()
        if user and verify_password(password, user.hashed_password):
            return user
        return None

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
