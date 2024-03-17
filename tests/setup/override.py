from fastapi import Depends, Request
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import TestSettings
from app.models.users import UserLoggedIn
from app.services.manger import ServiceManager
from tests.setup.test_models import get_mock_user_logged_in

settings = TestSettings()
uri = settings.TEST_MONGODB_CONNECT_STRING

async def override_get_db():
    db_client = AsyncIOMotorClient(uri)
    db = db_client[settings.TEST_DATABASE_NAME]
    try:
        yield db
    finally:
        await db_client.drop_database(settings.TEST_DATABASE_NAME)
        # db_client.close()

def override_get_current_user(request : Request, services : ServiceManager = Depends()) -> UserLoggedIn:
    return get_mock_user_logged_in()

async def override_validate_token(request: Request, call_next):
    return await call_next(request)
