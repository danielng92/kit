from fastapi import APIRouter, Depends
from app.api.auth import get_current_user
from app.models.users import ResponseUserModel, UserLoggedIn, UserModel
from app.services.manger import ServiceManager

user_router = APIRouter(prefix="/api/v1/user", tags=["User"])

@user_router.get("/{id}")
async def get_user(id: str, services: ServiceManager = Depends(), user: UserLoggedIn = Depends(get_current_user)) -> ResponseUserModel:
    user = await services.user.get_by_id(id)
    return user

@user_router.get("/")
async def get_users(services: ServiceManager = Depends(), user: UserLoggedIn = Depends(get_current_user)) -> list[ResponseUserModel]:
    print(user)
    users = await services.user.get_all()
    print(users)
    return users

@user_router.post("/")
async def create_user(user: UserModel, services: ServiceManager = Depends()):
    user = await services.user.create(user)
    return user

@user_router.put("/{id}")
async def update_user(id: str, user: UserModel, services: ServiceManager = Depends(), user_login: UserLoggedIn = Depends(get_current_user)):
    return await services.user.update(id, user)

@user_router.delete("/{id}")
async def update_user(id: str, services: ServiceManager = Depends(), user_login: UserLoggedIn = Depends(get_current_user)):
    return await services.user.remove(id)
