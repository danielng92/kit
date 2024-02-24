from app.services.user import UserService
from app.repositories.manger import RepositoryManager
from typing import Annotated
from fastapi import Depends
class ServiceManager:
    _repo: RepositoryManager
    _user: UserService

    def __init__(self, repo: RepositoryManager = Depends()) -> None:
        self._repo = repo
        self._user = None

    @property
    def user(self) -> UserService:
        if(self._user is None):
            self._user = UserService(self._repo)
        return self._user
    