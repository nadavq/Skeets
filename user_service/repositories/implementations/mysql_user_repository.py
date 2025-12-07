from user_service.model.user import User
from user_service.repositories.user_repository import IUserRepository


class MySqlUserRepository(IUserRepository):

    def create_user(self, user: User) -> User:
        pass

    def get_user_by_email(self, email: str) -> User:
        pass

    def get_user(self, user_id: str):
        pass
