from bson import ObjectId
from fastapi.testclient import TestClient
import pytest
from app.api.auth import get_current_user
from app.main import app, validate_token
from app.config.mongodb import get_db
from app.config.settings import TestSettings
from app.models.users import UserModel
from tests.setup.override import override_get_current_user, override_get_db, override_validate_token
from tests.setup.setup_db_models import setup_db_standard_test_models
from tests.setup.test_models import get_user_test

client = TestClient(app)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[validate_token] = override_validate_token
app.dependency_overrides[get_current_user] = override_get_current_user

url_path = "/api/v1/user/"


@pytest.mark.asyncio
async def test_delete_user_by_id_success() -> None:
    user_id, conver_id, message_id = await setup_db_standard_test_models()

    respone = client.delete(url_path + user_id)

    assert respone.status_code== 200

@pytest.mark.asyncio
async def test_create_already_exist_user_bad_request() -> None:
    user_id, conver_id, message_id =await setup_db_standard_test_models()
    user_dict = get_user_test()
    user = UserModel(**user_dict)
    respone= client.post(url_path, json=user.__dict__)

    assert respone.status_code== 400

@pytest.mark.asyncio
async def test_create_new_user_success() -> None:
    user_dict = get_user_test()
    user = UserModel(**user_dict)
    respone= client.post(url_path, json=user.__dict__)

    assert respone.status_code== 200

@pytest.mark.asyncio
async def test_get_random_id_not_found() -> None:
    user_id, conver_id, message_id = await setup_db_standard_test_models()
    randomId = ObjectId()
    respone = client.get(url_path + str(randomId))

    assert respone.status_code== 404

@pytest.mark.asyncio
async def test_get_user_by_id_success() -> None:
    user_id, conver_id, message_id = await setup_db_standard_test_models()

    respone = client.get(url_path + user_id)

    assert respone.status_code== 200