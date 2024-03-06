from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient
import pytest
from app.config.mongodb import get_db
from app.config.settings import TestSettings
from app.main import app
from app.models.conversations import ConversationModel
from app.models.messages import MessageModel
from app.models.users import UserModel
from app.repositories.message import MessageRepository
from bson import ObjectId

from app.utils.serialize import convert_conversations_to_mongo_data

client = TestClient(app)
settings = TestSettings()
uri = settings.TEST_MONGODB_CONNECT_STRING
message_test: MessageModel = MessageModel(sender_id="sender_id", content="test message", conversation_id="conversation id", read_by=["user_id_1","user_id_2"])

def override_get_db():
    db_client = AsyncIOMotorClient(uri)
    db = db_client[settings.TEST_DATABASE_NAME]
    try:
        yield db
    finally:
        db_client.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
async def setup_two_user():
    client = AsyncIOMotorClient(uri)
    db = client["kit_test"]
    collection = db["users"]

    #Arrange
    user1 = UserModel(username="username1", password="password",fullname="fullname1", email="email1@gmail.com", avatar="avatar")
    user2 = UserModel(username="username2", password="password",fullname="fullname2", email="email2@gmail.com", avatar="avatar")
    test_user_1 = await collection.insert_one(user1.model_dump())
    test_user_2 = await collection.insert_one(user2.model_dump())
    try:
        yield (str(test_user_1.inserted_id), str(test_user_2.inserted_id))
    finally:
        pass
        # await client.drop_database("kit_test")

@pytest.fixture(scope="module")
async def setup_conversation(setup_two_user):
    client = AsyncIOMotorClient(uri)
    db = client["kit_test"]
    collection = db["conversations"]

    #Arrange
    async for user_id_1, user_id_2 in setup_two_user:
        conversation = ConversationModel(is_channel=False, users=[user_id_1, user_id_2], group_admin=user_id_1, channel_name="conversation", latest_message="65c4bdbd716e58ad323acf2d")
        test_conversation = await collection.insert_one(convert_conversations_to_mongo_data(conversation))
        try:
            yield (user_id_1, user_id_2, str(test_conversation.inserted_id))
        finally:
            pass
            # await client.drop_database("kit_test")

@pytest.fixture(scope="module")
async def setup_one_message(setup_conversation):
    client = AsyncIOMotorClient(uri)
    db = client["kit_test"]
    collection = db["messages"]

    #Arrange
    async for user_id_1, user_id_2, conversation_id in setup_conversation:
        message = MessageModel(sender_id=user_id_1, content="message1", conversation_id=conversation_id, read_by=[user_id_1, user_id_2])
        result = await collection.insert_one(message.model_dump())

        try:
            yield (collection, result.inserted_id)
        finally:
            pass
            # await client.drop_database(settings.TEST_DATABASE_NAME)

@pytest.fixture(scope="module")
async def setup_two_message(setup_conversation):
    client = AsyncIOMotorClient(uri)
    db = client["kit_test"]
    collection = db["messages"]

    #Arrange
    async for user_id_1, user_id_2, conversation_id in setup_conversation:
        message1 = MessageModel(sender_id=user_id_1, content="message1", conversation_id=conversation_id, read_by=[user_id_1, user_id_2])
        message2 = MessageModel(sender_id=user_id_1, content="message2", conversation_id=conversation_id, read_by=[user_id_1, user_id_2])
        await collection.insert_one(message1.model_dump())
        await collection.insert_one(message2.model_dump())
        try:
            yield collection
        finally:
            pass 
            #await client.drop_database("kit_test")

# @pytest.mark.asyncio
# async def test_get_message_by_id(setup_one_message) -> None:
#     #Act
#     async for collection_test, message_id in setup_one_message:
#         repo = MessageRepository(collection_test)
#         doc = await repo.get_by_id(message_id)
#         message = MessageModel(**doc)
#         #Assert
#         assert message.content == "message1 wrong"

# @pytest.mark.asyncio
# async def test_get_all(setup_two_message) -> None:
#     #Act
#     async for collection_test in setup_two_message:
#         repo = MessageRepository(collection_test)
#         docs = await repo.get_all()
#         doc1 = docs[0]
#         doc2 = docs[1]
#         message1 = MessageModel(**doc1)
#         message2 = MessageModel(**doc2)

#         #Assert
#         assert len(docs) == 2
#         assert message1.content == "message1 wrong"
#         assert message2.content == "message2"

# @pytest.mark.asyncio
# async def test_create_message(setup_one_message) -> None:
#     #Act
#     async for collection_test, message_id in setup_one_message:
#         repo = MessageRepository(collection_test)
#         result = await repo.create(message_test)
#         message_just_created_dict = await repo.get_by_id(result.inserted_id)
#         message_just_created = MessageModel(**message_just_created_dict)
#         #Assert
#         assert message_just_created.content == "test message"

# @pytest.mark.asyncio
# async def test_update_message(setup_one_message) -> None:
#     #Arrange
#     async for collection_test, message_id in setup_one_message:
#         repo = MessageRepository(collection_test)
#         doc = await repo.get_by_id(message_id)
#         message = MessageModel(**doc)
#         message.content = "message updated"
#         #Act
#         await repo.update(message_id, message)

#         doc = await repo.get_by_id(message_id)
#         message_after_update = MessageModel(**doc)
#         #Assert
#         assert message_after_update.content == "message updated"

# @pytest.mark.asyncio
# async def test_remove_message(setup_one_message) -> None:
#     #Arrange
#     async for collection_test, message_id in setup_one_message:
#         repo = MessageRepository(collection_test)
#         await repo.remove(message_id)
#         list = await repo.get_all()
#         #Assert
#         assert list == None

# @pytest.mark.asyncio
# async def test_get_message_by_conversation_id(setup_two_message, setup_conversation) -> None:
#     #Arrange
#     async for collection_test in setup_two_message:
#         async for conversation_id in setup_conversation:
#             repo = MessageRepository(collection_test)
#             docs = await repo.get_by_conversation_id(conversation_id)
#             doc1 = docs[0]
#             message1 = MessageModel(**doc1)

#             #Assert
#             assert len(docs) == 2
#             assert message1.content == "wrong message" #right is mesage1