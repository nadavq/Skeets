from user_service.model.user import User
from user_service.repositories.user_repository import IUserRepository


class MySqlUserRepository(IUserRepository):

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).where(User.email == email).first()

    def get_user(self, user_id: str):
        return self.db.get(User, user_id)
