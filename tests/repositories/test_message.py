from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient
import pytest
from app.config.mongodb import get_db
from app.config.settings import TestSettings
from app.main import app
from app.models.conversations import ConversationModel
from app.models.messages import MessageModel, ResponseMessageModel
from app.models.users import UserModel
from app.repositories.message import MessageRepository
from bson import ObjectId

from app.utils.conver_mongo_data import convert_conversations_to_mongo_data, convert_message_to_mongo_data, convert_message_to_py_data

client = TestClient(app)
settings = TestSettings()
uri = settings.TEST_MONGODB_CONNECT_STRING
message_test: MessageModel = MessageModel(sender_id="65bb4bced574c97a05eea7f4", content="test message", conversation_id="65bb4bced574c97a05eea7f4", read_by=["65bb4bced574c97a05eea7f4","65bb4e5da6f263f58e50e3eb"])

def override_get_db():
    db_client = AsyncIOMotorClient(uri)
    db = db_client[settings.TEST_DATABASE_NAME]
    try:
        yield db
    finally:
        db_client.close()

app.dependency_overrides[get_db] = override_get_db

async def setup_two_user():
    client = AsyncIOMotorClient(uri)
    db = client[settings.TEST_DATABASE_NAME]
    collection = db["users"]

    #Arrange
    user1 = UserModel(username="username1", password="password",fullname="fullname1", email="email1@gmail.com", avatar="avatar")
    user2 = UserModel(username="username2", password="password",fullname="fullname2", email="email2@gmail.com", avatar="avatar")
    test_user_1 = await collection.insert_one(user1.model_dump())
    test_user_2 = await collection.insert_one(user2.model_dump())
    try:
        yield (str(test_user_1.inserted_id), str(test_user_2.inserted_id))
    finally:
        await client.drop_database(settings.TEST_DATABASE_NAME)

async def setup_conversation():
    client = AsyncIOMotorClient(uri)
    db = client[settings.TEST_DATABASE_NAME]
    collection = db["conversations"]

    #Arrange
    async for user_id_1, user_id_2 in setup_two_user():
        conversation = ConversationModel(is_channel=False, users=[user_id_1, user_id_2], group_admin=user_id_1, channel_name="conversation", latest_message="65c4bdbd716e58ad323acf2d")
        test_conversation = await collection.insert_one(convert_conversations_to_mongo_data(conversation))
        try:
            yield (user_id_1, user_id_2, str(test_conversation.inserted_id))
        finally:
            await client.drop_database(settings.TEST_DATABASE_NAME)

async def setup_two_conversation():
    client = AsyncIOMotorClient(uri)
    db = client[settings.TEST_DATABASE_NAME]
    collection = db["conversations"]

    #Arrange
    async for user_id_1, user_id_2 in setup_two_user():
        conversation_one = ConversationModel(is_channel=False, users=[user_id_1, user_id_2], group_admin=user_id_1, channel_name="conversation", latest_message="65c4bdbd716e58ad323acf2d")
        conversation_two = ConversationModel(is_channel=False, users=[user_id_1, user_id_2], group_admin=user_id_1, channel_name="conversation 2", latest_message="65c4bdbd716e58ad323acf2d")
        test_conversation_one = await collection.insert_one(convert_conversations_to_mongo_data(conversation_one))
        test_conversation_two = await collection.insert_one(convert_conversations_to_mongo_data(conversation_two))
        try:
            yield (user_id_1, user_id_2, str(test_conversation_one.inserted_id), str(test_conversation_two.inserted_id))
        finally:
            await client.drop_database(settings.TEST_DATABASE_NAME)

async def setup_one_message():
    client = AsyncIOMotorClient(uri)
    db = client[settings.TEST_DATABASE_NAME]
    collection = db["messages"]

    #Arrange
    async for user_id_1, user_id_2, conversation_id in setup_conversation():
        message = MessageModel(sender_id=user_id_1, content="message1", conversation_id=conversation_id, read_by=[user_id_1, user_id_2])
        result = await collection.insert_one(convert_message_to_mongo_data(message))

        try:
            yield (collection, str(result.inserted_id))
        finally:
            await client.drop_database(settings.TEST_DATABASE_NAME)

async def setup_two_message():
    client = AsyncIOMotorClient(uri)
    db = client[settings.TEST_DATABASE_NAME]
    collection = db["messages"]

    #Arrange
    async for user_id_1, user_id_2, conversation_id in setup_conversation():
        message1 = MessageModel(sender_id=user_id_1, content="message1", conversation_id=conversation_id, read_by=[user_id_1, user_id_2])
        message2 = MessageModel(sender_id=user_id_1, content="message2", conversation_id=conversation_id, read_by=[user_id_1, user_id_2])
        await collection.insert_one(convert_message_to_mongo_data(message1))
        await collection.insert_one(convert_message_to_mongo_data(message2))
        try:
            yield collection
        finally:
            await client.drop_database(settings.TEST_DATABASE_NAME)

async def setup_three_message():
    client = AsyncIOMotorClient(uri)
    db = client[settings.TEST_DATABASE_NAME]
    collection = db["messages"]

    #Arrange
    async for user_id_1, user_id_2, conversation_id_one, conversation_id_two in setup_two_conversation():
        #in conversation 1 have 2 message
        message1 = MessageModel(sender_id=user_id_1, content="message1", conversation_id=conversation_id_one, read_by=[user_id_1, user_id_2])
        message2 = MessageModel(sender_id=user_id_1, content="message2", conversation_id=conversation_id_one, read_by=[user_id_1, user_id_2])

        await collection.insert_one(convert_message_to_mongo_data(message1))
        await collection.insert_one(convert_message_to_mongo_data(message2))

        #in conversation 2 have 1 message
        message3 = MessageModel(sender_id=user_id_1, content="message2", conversation_id=conversation_id_two, read_by=[user_id_1, user_id_2])
        await collection.insert_one(convert_message_to_mongo_data(message3))

        try:
            yield (collection, conversation_id_one, conversation_id_two)
        finally:
            await client.drop_database(settings.TEST_DATABASE_NAME)   

@pytest.mark.asyncio
async def test_get_message_by_id() -> None:
    #Act
    async for collection_test, message_id in setup_one_message():
        repo = MessageRepository(collection_test)
        doc = await repo.get_by_id(message_id)
        message = ResponseMessageModel(**doc)
    #Assert
    assert message.content == "message1" #Already test the wrong case "message1 wrong"

@pytest.mark.asyncio
async def test_get_all() -> None:
    #Act
    async for collection_test in setup_two_message():
        repo = MessageRepository(collection_test)
        docs = await repo.get_all()
        doc1 = docs[0]
        doc2 = docs[1]
        message1 = ResponseMessageModel(**doc1)
        message2 = ResponseMessageModel(**doc2)

    #Assert
    assert len(docs) == 2
    assert message1.content == "message1" #Already test the wrong case "message1 wrong"
    assert message2.content == "message2"

@pytest.mark.asyncio
async def test_create_message() -> None:
    #Act
    async for collection_test, message_id in setup_one_message():
        repo = MessageRepository(collection_test)
        result = await repo.create(message_test)
        message_just_created_dict = await repo.get_by_id(result.inserted_id)
        message_just_created = ResponseMessageModel(**message_just_created_dict)
    #Assert
    assert message_just_created.content == "test message" #Already test the wrong case "test message wrong"

@pytest.mark.asyncio
async def test_update_message() -> None:
    #Arrange
    async for collection_test, message_id in setup_one_message():
        repo = MessageRepository(collection_test)
        doc = await repo.get_by_id(message_id)
        message = ResponseMessageModel(**doc)
        message.content = "message updated"
        #Act
        await repo.update(message_id, convert_message_to_py_data(message))

        doc = await repo.get_by_id(message_id)
        message_after_update = ResponseMessageModel(**doc)
    #Assert
    assert message_after_update.content == "message updated" #Already test the wrong case "message updated wrong"

@pytest.mark.asyncio
async def test_remove_message() -> None:
    #Arrange
    async for collection_test, message_id in setup_one_message():
        repo = MessageRepository(collection_test)
        await repo.remove(message_id)
        list = await repo.get_all()
    #Assert
    assert list == None #Already test the wrong case "!= None"

@pytest.mark.asyncio
async def test_get_message_by_conversation_id() -> None:
    #Arrange
    async for collection_test, conversation_id_one, conversation_id_two in setup_three_message():
        repo = MessageRepository(collection_test)
        docs_1 = await repo.get_by_conversation_id(conversation_id_one)
        docs_2 = await repo.get_by_conversation_id(conversation_id_two)

    #Assert
    assert len(docs_1) == 2 #Already test the wrong case "len(docs_1) == 3"
    assert len(docs_2) == 1