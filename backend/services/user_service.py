from ..models.user import UserLogin, UserOut

class UserService:
    def login(self, user: UserLogin) -> UserOut:
        # Заглушка
        return UserOut(id=1, email=user.email, verified=True)
