from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.repositories.manger import RepositoryManager
from app.models.users import UserModel

user_router = APIRouter(prefix="/api/v1/user", tags=["User"])

@user_router.get("/{id}")
async def get_user(id: str, repositories: RepositoryManager = Depends()) -> dict:
    user = await repositories.user.get_by_id(id)
    return user

@user_router.get("/")
async def get_users(repositories: RepositoryManager = Depends()) -> list[UserModel]:
    users = await repositories.user.get_all()
    return users

@user_router.post("/")
async def create_user(user: UserModel, repositories: RepositoryManager = Depends()):
    await repositories.user.create(dict(user))
    return HTTPStatus.NO_CONTENT

@user_router.put("/{id}")
async def update_user(id: str, user: UserModel, repositories: RepositoryManager = Depends()):
    await repositories.user.update(id, user)
    return HTTPStatus.NO_CONTENT

@user_router.delete("/{id}")
async def update_user(id: str, repositories: RepositoryManager = Depends()):
    await repositories.user.remove(id)
    return HTTPStatus.NO_CONTENT
