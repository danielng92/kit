from fastapi import Depends
from app.models.users import UserModel
from app.repositories.manger import RepositoryManager


class UserService():
    def __init__(self, repositories: RepositoryManager = Depends()) -> None:
        self.repositories = repositories

    async def get_by_id(self, id: str):
        user = await self.repositories.user.get_by_id(id)
        if user is None:
            return {"message": "Not Found User"}
        else:
            return user

    async def get_all(self):
        return await self.repositories.user.get_all()
    
    async def create(self, user: UserModel):
        existed_user_by_email = await self.repositories.user.get_by_email(user.email)
        if existed_user_by_email is None:
            await self.repositories.user.create(user)
            new_user = await self.repositories.user.get_by_email(user.email)
            return new_user
        else:
            return {"message": f"User with email '{user.email}' already exists"}

    async def update(self, id: str,  user: UserModel):
        existed_user_by_id = await self.repositories.user.get_by_id(id)
        existed_user_by_email = await self.repositories.user.get_by_email(user.email)
        print(existed_user_by_id.get("_id"))
        if existed_user_by_id is None:
            return {"message": f"User with id '{id}' is not exist"}
        if existed_user_by_id and existed_user_by_email and existed_user_by_id.get("_id") != existed_user_by_email.get("_id"):
            return {"message": f"User with email already used"}
        else:
            await self.repositories.user.update(id, user)
            return {"message": f"Update success"}

    async def remove(self, id: str):
        existed_user_by_id = await self.repositories.user.get_by_id(id)
        if existed_user_by_id is None:
            return {"message": f"User with id '{id}' is not exist"}
        else:
            await self.repositories.user.remove(id)
            return {"message": f"User with id '{id}' deleted"}