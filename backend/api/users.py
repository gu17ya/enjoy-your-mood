from fastapi import APIRouter
from ..models.user import UserLogin, UserOut
from ..services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

user_service = UserService()

@router.post("/login", response_model=UserOut)
def login(user: UserLogin):
    return user_service.login(user)