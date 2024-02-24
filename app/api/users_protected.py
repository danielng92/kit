from fastapi import APIRouter, Depends

from app.config.mongodb import get_db
from .auth import authorize_class
from app.models.users import UserModel
from app.repositories.manger import RepositoryManager

def get_repository_manager(db = Depends(get_db)) -> RepositoryManager:
    return RepositoryManager(db)
# Class definition
# For Developing purpose
@authorize_class
class UserProtected:
    def __init__(self, repositories: RepositoryManager) -> None:
        self.router = APIRouter(prefix="/api/v1/user-protected", tags=["User-protected"])
        self.router.add_api_route("/hello", self.hello, methods=["GET"])
        self.router.add_api_route("/{id}", self.get_user, methods=["GET"])
        self.router.add_api_route("/", self.get_users, methods=["GET"])
        self.repositories = repositories
    
    async def hello(self):
        return {"hello"}
    
    async def get_user(self, id: str) -> dict:
        user = await self.repositories.user.get_by_id(id)
        return user

    async def get_users(self) -> list[UserModel]:
        users = await self.repositories.user.get_all()
        return users