from pydantic import BaseModel, EmailStr, Field

class UserModel(BaseModel):
    username: str = None
    password: str = None
    fullname: str = None
    email: EmailStr
    avatar: str = None

class ResponseUserModel(UserModel):
    id: str = Field(alias="_id")