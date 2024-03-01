
from bson import ObjectId
from app.models.messages import MessageModel
from app.repositories.base import BaseRepository
from app.utils.serialize import serialize_dict, serialize_list


class MessageRepository(BaseRepository):
    def __init__(self,message_collection)-> None:
        self.message_collection = message_collection
    
    async def get_by_id(self, id: str) ->dict:
        return serialize_dict(await self.message_collection.find_one({"_id": ObjectId(id)}))
    
    async def get_all(self):
        return await serialize_list(self.message_collection.find())
    
    async def create(self, message: MessageModel):
        await self.message_collection.insert_one(message)

    async def update(self, id: str, message: MessageModel):
        await self.message_collection.update_one({"_id": ObjectId(id)}, {"$set": dict(message)})

    async def remove(self, id: str):
        await self.message_collection.delete_one({"_id": ObjectId(id)})

    async def get_by_conversation_id(self, id:str) ->list:
        return await serialize_list(self.message_collection.find({"conversation_id": ObjectId(id)}))