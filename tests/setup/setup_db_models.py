
from bson import ObjectId
from app.config.settings import TestSettings
from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.conver_mongo_data import convert_conversations_to_mongo_data, convert_message_to_mongo_data
from tests.setup.test_models import get_conversation_test, get_message_test, get_user_test


settings = TestSettings()
uri = settings.TEST_MONGODB_CONNECT_STRING

async def setup_db_standard_test_models() -> tuple[str, str, str]:
    users_collection, conversation_collection, message_collection = get_collections()
    
    #USER
    user = get_user_test()
    user_created = await users_collection.insert_one(user)

    #CONVERSATION
    conversation = get_conversation_test(str(user_created.inserted_id))
    conversation_created = await conversation_collection.insert_one(convert_conversations_to_mongo_data(conversation))

    #Message
    message = get_message_test(str(user_created.inserted_id), str(conversation_created.inserted_id))
    message_created = await message_collection.insert_one(convert_message_to_mongo_data(message))
    
    return str(user_created.inserted_id), str(conversation_created.inserted_id), str(message_created.inserted_id)

async def setup_db_user_not_belongto_conversation_test_models() -> tuple[str, str, str]:
    users_collection, conversation_collection, message_collection = get_collections()
    
    #USER
    user = get_user_test()
    user_created = await users_collection.insert_one(user)

    #CONVERSATION
    randomId = ObjectId()
    conversation = get_conversation_test(str(randomId))
    conversation_created = await conversation_collection.insert_one(convert_conversations_to_mongo_data(conversation))

    #Message
    message = get_message_test(str(randomId), str(conversation_created.inserted_id))
    message_created = await message_collection.insert_one(convert_message_to_mongo_data(message))
    
    return str(user_created.inserted_id), str(conversation_created.inserted_id), str(message_created.inserted_id)

def get_collections():
    client = AsyncIOMotorClient(uri)
    db = client[settings.TEST_DATABASE_NAME]
    users_collection = db["users"]
    conversation_collection = db["conversations"]
    message_collection = db["messages"]
    return users_collection,conversation_collection,message_collection