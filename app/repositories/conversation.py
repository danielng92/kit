from app.utils.conver_mongo_data import convert_conversations_to_mongo_data
from app.utils.serialize import serialize_dict, serialize_list
from .base import BaseRepository
from bson import ObjectId
from app.models.conversations import ConversationModel

class ConversationRepository(BaseRepository):
    def __init__(self, conversations_collection) -> None:
        self.conversations_collection = conversations_collection

    async def get_by_id(self, id: str) -> dict:
        return serialize_dict(await self.conversations_collection.find_one({"_id": ObjectId(id)}))
    
    async def get_by_id_all_info(self, id: str) -> dict:
        aggregation = [
            {"$match": {"_id": ObjectId(id)}},
            {"$lookup": {
                "from": "users",  # Join with users collection
                "localField": "users",  # Match user IDs
                "foreignField": "_id",  # On user document IDs
                "as": "users"  # Alias for matched users
            }},
            {"$lookup": {
                "from": "users",  # Join with user collection again
                "localField": "group_admin",  # Match admin ID
                "foreignField": "_id",  # On user document IDs
                "as": "group_admin"  # Alias for matched admin
            }},
            {"$lookup": {
                "from": "messages",  # Join with user collection again
                "localField": "latest_message",  # Match admin ID
                "foreignField": "_id",  # On user document IDs
                "as": "latest_message"  # Alias for matched admin
            }},
            {"$unwind": "$group_admin"},  # Flatten the adminGroup array
            {"$project": {"_id": 1, "is_channel":1, "channel_name":1, "latest_message":1, "users": 1, "group_admin": 1}}  # Include only relevant fields
        ]
        cursor = self.conversations_collection.aggregate(aggregation)
        conversation = await cursor.to_list(None)
        return serialize_dict(conversation[0])
    
    async def get_all(self):
        return await serialize_list(self.conversations_collection.find())
    
    async def create(self, conversation: ConversationModel):
        await self.conversations_collection.insert_one(convert_conversations_to_mongo_data(conversation))

    async def update(self, id: str, conversation: ConversationModel):
        await self.conversations_collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": convert_conversations_to_mongo_data(conversation)})

    async def remove(self, id: str): 
        await self.conversations_collection.delete_one({"_id": ObjectId(id)})
