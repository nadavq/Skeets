from pydantic import BaseModel


class JwtTokenRead(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class ForgotPasswordRequest(BaseModel):
    email: str
