from ast import Dict
from typing import Optional
from app.utils.serialize import serialize_dict, serialize_list
from .base import BaseRepository
from bson import ObjectId
from app.models.users import ResponseUserModel, UserModel

class UserRepository(BaseRepository):
    def __init__(self, users_collection) -> None:
        self.users_collection = users_collection

    async def get_by_id(self, id: str) -> dict:
        return serialize_dict(await self.users_collection.find_one({"_id": ObjectId(id)}))
     
    async def get_by_email(self, email: str) -> dict:
        return serialize_dict(await self.users_collection.find_one({"email": email}))

    async def get_all(self) -> list:
        return await serialize_list(self.users_collection.find())

    async def create(self, user: UserModel):
        await self.users_collection.insert_one(dict(user))

    async def update(self, id: str,  user: UserModel):
        await self.users_collection.update_one({"_id": ObjectId(id)}, {"$set": dict(user)})

    async def remove(self, id: str):
        await self.users_collection.delete_one({"_id": ObjectId(id)})