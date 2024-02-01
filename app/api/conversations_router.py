from fastapi import APIRouter
from models.conversations import ConversationModel
from motor.motor_asyncio import AsyncIOMotorClient
from config.mongodb import conversations_collection
from utils.conversations_serialize import individual_conversation
from bson.objectid import ObjectId

client = AsyncIOMotorClient("mongodb+srv://admin:admin123@cluster0.sizb9bz.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB URI
db = client["kit"]  # Replace with your database name

conversations_router = APIRouter()
@conversations_router.post("/conversation")
async def create_conversation(conversation: ConversationModel):
    conversation = conversations_collection.insert_one(
        {
            "is_channel": conversation.is_channel,
            "users": [ObjectId(user_id) for user_id in conversation.users],
            "group_admin": ObjectId(conversation.group_admin),
            "latest_message": conversation.latest_message,
            "channel_name": conversation.channel_name,
        }
    )
    return {"message": "create new conversation successful"}

@conversations_router.get("/conversations/{id}")
async def get_conversation(id: str):
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
        {"$unwind": "$group_admin"},  # Flatten the adminGroup array
        {"$project": {"_id": 1, "is_channel":1, "channel_name":1, "latest_message":1, "users": 1, "group_admin": 1}}  # Include only relevant fields
    ]
    conversation = dict(conversations_collection.aggregate(aggregation))
    return individual_conversation(conversation[0])