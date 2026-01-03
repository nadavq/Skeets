import datetime

from fastapi import HTTPException

from core.security import pwd_context
from core.repositories_dependencies import get_user_repository, DbType, curr_db_type
from model.user import User
from repositories.user_repository import IUserRepository
from schema.user import UserCreate, UserRead, UserEdit


class UserService:
    def __init__(self, db):
        self.db = db
        self.users: IUserRepository = get_user_repository(db)

    def create_user(self, user_create: UserCreate) -> UserRead:
        try:
            hashed_password = pwd_context.hash(user_create.password)
            now = datetime.datetime.now()
            user = User(
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                email=str(user_create.email),
                password=hashed_password,
                creation_time=now,
                last_update_time=now
            )
            new_user = self.users.create_user(user)
            
            # Only commit and refresh for SQLAlchemy (MySQL), not for MongoDB
            if curr_db_type == DbType.MYSQL:
                self.db.commit()
                self.db.refresh(new_user)
            
            return UserRead.model_validate(new_user)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_user_by_email(self, email: str) -> UserRead:
        user = self.users.get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return UserRead.model_validate(user)

    def get_user(self, user_id: str):
        return self.users.get_user(user_id)

    def edit_user(self, user_id: str, user: UserEdit) -> UserRead:
        current_user = self.users.get_user(user_id)
        current_user.flashcards_side = user.flashcards_side
        self.users.edit_user(current_user)
        user_edited = self.get_user(user_id)
        return UserRead.model_validate(user_edited)