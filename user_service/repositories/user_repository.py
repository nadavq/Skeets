from abc import ABC, abstractmethod

from user_service.model.user import User


class IUserRepository(ABC):

    def __init__(self, db):
        self.db = db

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass
