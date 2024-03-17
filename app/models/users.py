from pydantic import BaseModel, EmailStr, Field
from typing import Any

class UserModel(BaseModel):
    username: str = None
    password: str = None
    fullname: str = None
    email: EmailStr
    avatar: str = None

class ResponseUserModel(UserModel):
    id: str = Field(alias="_id")

class UserLoggedIn(BaseModel):
    id: str = None
    iss: str = None
    azp: str = None
    aud: str = None
    sub: str = None
    email: str = None
    email_verified: int = None
    at_hash: str = None
    nonce: str = None
    name: str = None
    picture: str = None
    given_name: str = None
    family_name: str = None
    locale: str = None
    iat: int = None
    exp: int = None