import datetime
import os
from datetime import datetime
from datetime import timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi import Response
from jose import jwt

from user_service.core.repositories_dependencies import get_user_repository
from user_service.db.db import db_dep
from user_service.exceptions.AuthException import AuthException
from user_service.model.user import User
from shared.security import pwd_context
from user_service.repositories.implementations.mysql_user_repository import IUserRepository
from user_service.schema.auth import JwtTokenRead
from user_service.security import oauth2_bearer

load_dotenv()
IS_PROD = os.getenv("ENV") == "production"


def create_access_token(user: User) -> JwtTokenRead:
    encode = {'sub': user.email, 'id': user.id}
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    encode.update({'exp': expires})
    secret_key = os.environ.get("JWT_SECRET_KEY")
    token = jwt.encode(encode, secret_key, algorithm='HS256')
    return JwtTokenRead(access_token=token)


class AuthService:
    def __init__(self, db):
        self.db = db
        self.users: IUserRepository = get_user_repository(db)

    def authenticate_user(self, username: str, password: str, response: Response) -> JwtTokenRead:
        try:
            user = self.users.get_user_by_email(username)
            if user is None:
                raise AuthException(f'The user with email {username} was not found')
            elif not pwd_context.verify(password, user.password):
                raise Exception('Email or password incorrect')

            token_obj = create_access_token(user)
            return token_obj
        except AuthException as ae:
            raise HTTPException(status_code=401, detail=str(ae))
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_current_user(self, token: str) -> str:
        secret_key = os.environ.get("JWT_SECRET_KEY")
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')

        if not username or not user_id:
            raise Exception('Invalid token')

        return user_id

    def forgot_password(self, email: str):
        print(str(email))
        return email


def get_auth_service(db: db_dep):
    return AuthService(db)


def current_user_id(token: str = Depends(oauth2_bearer), auth_service: AuthService = Depends(get_auth_service)) -> str:
    try:
        return auth_service.get_current_user(token)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
