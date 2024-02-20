from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient
import pytest
from app.config.mongodb import get_db
from app.config.settings import TestSettings
from app.main import app
from app.models.users import UserModel
from app.repositories.user import UserRepository

client = TestClient(app)
settings = TestSettings()
uri = settings.TEST_MONGODB_CONNECT_STRING
user_test: UserModel = UserModel(username="test", password="test",fullname="test", email="email@gmail.com", avatar="avatar")

def override_get_db():
    db_client = AsyncIOMotorClient(uri)
    db = db_client[settings.TEST_DATABASE_NAME]
    try:
        yield db
    finally:
        db_client.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
async def setup_one_user():
    client = AsyncIOMotorClient(uri)
    db = client[settings.TEST_DATABASE_NAME]
    collection = db["users"]

    #Arrange
    user = UserModel(username="username", password="password",fullname="fullname2", email="email@gmail.com", avatar="avatar")
    result = await collection.insert_one(user.model_dump())

    try:
       yield (collection, result.inserted_id)
    finally:
       await client.drop_database(settings.TEST_DATABASE_NAME)

@pytest.fixture(scope="module")
async def setup_two_user():
    client = AsyncIOMotorClient(uri)
    db = client["kit_test"]
    collection = db["users"]

    #Arrange
    user1 = UserModel(username="username1", password="password",fullname="fullname2", email="email@gmail.com", avatar="avatar")
    user2 = UserModel(username="username2", password="password",fullname="fullname2", email="email@gmail.com", avatar="avatar")
    await collection.insert_one(user1.model_dump())
    await collection.insert_one(user2.model_dump())

    try:
        yield collection
    finally:
        await client.drop_database("kit_test")

@pytest.mark.asyncio
async def test_get_user_by_id(setup_one_user) -> None:
    #Act
    async for collection_test, user_id in setup_one_user:
        repo = UserRepository(collection_test)
        doc = await repo.get_by_id(user_id)
        user = UserModel(**doc)
        #Assert
        assert user.username == "username"

@pytest.mark.asyncio
async def test_get_all(setup_two_user) -> None:
    #Act
    async for collection_test in setup_two_user:
        repo = UserRepository(collection_test)
        docs = await repo.get_all()
        doc1 = docs[0]
        doc2 = docs[1]
        user1 = UserModel(**doc1)
        user2 = UserModel(**doc2)
        #Assert
        assert len(docs) == 2
        assert user1.username == "username1"
        assert user2.username == "username2"

@pytest.mark.asyncio
async def test_create_user(setup_one_user) -> None:
    #Act
    async for collection_test, user_id in setup_one_user:
        repo = UserRepository(collection_test)
        result = await repo.create(user_test)
        user_just_created_dict = await repo.get_by_id(result.inserted_id)
        user_just_created = UserModel(**user_just_created_dict)
        #Assert
        assert user_just_created.username == "test"

@pytest.mark.asyncio
async def test_user_update(setup_one_user) -> None:
    #Arrange
    async for collection_test, user_id in setup_one_user:
        repo = UserRepository(collection_test)
        doc = await repo.get_by_id(user_id)
        user = UserModel(**doc)
        user.username = "changeusername"
        user.avatar = "changeavatar"
        user.email = "changeemail@gmail.com"
        user.fullname = "changefullname"
        user.password = "changepassword"
        #Act
        await repo.update(user_id, user)
        
        doc = await repo.get_by_id(user_id)
        user_after_update = UserModel(**doc)
        #Assert
        assert user_after_update.username == "changeusername"
        assert user_after_update.avatar == "changeavatar"
        assert user_after_update.email == "changeemail@gmail.com"
        assert user_after_update.fullname == "changefullname"
        assert user_after_update.password == "changepassword"

@pytest.mark.asyncio
async def test_user_remove(setup_one_user) -> None:
    #Arrange
    async for collection_test, user_id in setup_one_user:
        repo = UserRepository(collection_test)
        await repo.remove(user_id)
        list = await repo.get_all()
        #Assert
        assert list == None