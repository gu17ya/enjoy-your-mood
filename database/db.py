from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./database/users.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создаём все таблицы, описанные в моделях
Base.metadata.create_all(bind=engine)
