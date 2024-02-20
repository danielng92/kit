from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.repositories.manger import RepositoryManager
from app.models.users import ResponseUserModel, UserModel
from app.services.manger import ServiceManager

user_router = APIRouter(prefix="/api/v1/user", tags=["User"])

@user_router.get("/{id}")
async def get_user(id: str, services: ServiceManager = Depends()) -> dict:
    user = await services.user.get_by_id(id)
    return user

@user_router.get("/")
async def get_users(services: ServiceManager = Depends()) -> list[ResponseUserModel]:
    users = await services.user.get_all()
    return users

@user_router.post("/")
async def create_user(user: UserModel, services: ServiceManager = Depends()):
    user = await services.user.create(user)
    return user

@user_router.put("/{id}")
async def update_user(id: str, user: UserModel, services: ServiceManager = Depends()):
    return await services.user.update(id, user)

@user_router.delete("/{id}")
async def update_user(id: str, services: ServiceManager = Depends()):
    return await services.user.remove(id)
