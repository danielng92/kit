from fastapi import Depends
from app.common.exceptions.exceptions import BadRequestException, NotFoundException
from app.models.users import ResponseUserModel, UserModel
from app.repositories.manger import RepositoryManager


class UserService():
    def __init__(self, repositories: RepositoryManager) -> None:
        self.repositories = repositories

    async def get_by_id(self, id: str) -> ResponseUserModel:
        user = await self.repositories.user.get_by_id(id)
        if user is None:
            raise NotFoundException(f"Not found user with id: {id}")
        else:
            return ResponseUserModel(**user)

    async def get_all(self) -> list[ResponseUserModel]:
        return await self.repositories.user.get_all()
    
    async def create(self, user: UserModel) -> None:
        existed_user_by_email = await self.repositories.user.get_by_email(user.email)
        if existed_user_by_email is None:
            await self.repositories.user.create(user)
        else:
            raise BadRequestException(f"User with email '{user.email}' already exists")

    async def update(self, id: str,  user: UserModel) -> None:
        existed_user_by_id = await self.repositories.user.get_by_id(id)
        existed_user_by_email = await self.repositories.user.get_by_email(user.email)

        if existed_user_by_id is None:
            raise NotFoundException(f"Not found user with id: {id}")
        if existed_user_by_id and existed_user_by_email and ResponseUserModel(**existed_user_by_id).id != ResponseUserModel(**existed_user_by_email).id:
            raise BadRequestException(f"User with email '{user.email}' already used")
        else:
            await self.repositories.user.update(id, user)

    async def remove(self, id: str) -> None:
        existed_user_by_id = await self.repositories.user.get_by_id(id)
        if existed_user_by_id is None:
            raise NotFoundException(f"Not found user with id: {id}")
        else:
            await self.repositories.user.remove(id)