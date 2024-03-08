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
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: int
    at_hash: str
    nonce: str
    name: str
    picture: str
    given_name: str
    family_name: str
    locale: str
    iat: int
    exp: int