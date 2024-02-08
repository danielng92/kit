from pydantic import BaseModel, EmailStr, Field

class UserModel(BaseModel):
    username: str = None
    password: str = None
    fullname: str = None
    email: EmailStr
    avatar: str = None

class ResponseUserModel(BaseModel):
    id: str = Field(alias="_id")
    username: str = None
    password: str = None
    fullname: str = None
    email: EmailStr
    avatar: str = None