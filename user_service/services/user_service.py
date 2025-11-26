import datetime

from fastapi import HTTPException

from shared.security import pwd_context
from user_service.core.repositories_dependencies import get_user_repository, DbType, curr_db_type
from user_service.model.user import User
from user_service.repositories.user_repository import IUserRepository
from user_service.schema.user import UserCreate, UserRead


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
