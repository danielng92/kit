

from fastapi import Depends
from app.repositories.manger import RepositoryManager


class UserService():
    def __init__(self, repos_manager: RepositoryManager = Depends()) -> None:
        self.repos_manager = repos_manager

    async def get_all(self):
        return await self.repos_manager.user.get_all()