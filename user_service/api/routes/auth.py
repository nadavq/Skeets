from typing import Annotated

from fastapi import APIRouter, Response
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from user_service.db.db import db_dep
from user_service.schema.auth import JwtTokenRead, ForgotPasswordRequest
from user_service.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=JwtTokenRead)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dep, response: Response):
    return AuthService(db).authenticate_user(form_data.username, form_data.password, response)


@router.post("/forgot-password")
def forgot_password(forgot_password_request: ForgotPasswordRequest, db: db_dep):
    return AuthService(db).forgot_password(forgot_password_request.email)
