from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from backend.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

class UserIn(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: str
    email: str

@router.post("/register", response_model=UserOut)
def register(user: UserIn):
    service = UserService()
    try:
        new_user = service.register_user(user.email, user.password)
        return {"id": new_user["id"], "email": new_user["email"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=UserOut)
def login(user: UserIn, request: Request):
    service = UserService()
    auth_user = service.authenticate_user(user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    request.session["user_id"] = auth_user["id"]
    return {"id": auth_user["id"], "email": auth_user["email"]}
