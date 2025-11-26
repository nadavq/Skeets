from fastapi import APIRouter

from shared.common import user_dep
from user_service.db.db import db_dep
from user_service.schema.user import UserCreate, UserRead
from user_service.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/user")
def create_user(user_create: UserCreate, db: db_dep):
    return UserService(db).create_user(user_create)


@router.get("/me", response_model=UserRead)
def get_me(user_id: user_dep, db: db_dep):
    return UserService(db).get_user(user_id)


@router.get("/user-by-email/{email}", response_model=UserRead)
def get_user_by_email(email: str, db: db_dep) -> UserRead:
    return UserService(db).get_user_by_email(email)


@router.put("/")
def test(s):
    print(s)
