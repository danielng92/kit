from bson import ObjectId
from fastapi.testclient import TestClient
import pytest
from app.api.auth import get_current_user
from app.main import app, validate_token
from app.config.mongodb import get_db
from app.config.settings import TestSettings
from tests.setup.override import override_get_current_user, override_get_db, override_validate_token
from tests.setup.setup_db_models import setup_db_standard_test_models, setup_db_user_not_belongto_conversation_test_models
from tests.setup.test_models import get_message_test

client = TestClient(app)
settings = TestSettings()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[validate_token] = override_validate_token
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.mark.asyncio
async def test_message_get_by_id_success() -> None:
    #Arrange
    user_id, conver_id, message_id = await setup_db_standard_test_models()
    #Act
    response = client.get("/api/v1/message/"+ message_id)
    #Assert
    assert response.status_code == 200
    assert response.json() == {"sender_id": user_id,
                                "content": "test message",
                                "conversation_id": conver_id,
                                "read_by": [
                                    {
                                    "_id": user_id
                                    },
                                ],
                                "_id": message_id
                                }
@pytest.mark.asyncio
async def test_message_send_sender_id_not_match_user_id_forbiden() -> None:
    user_id, conver_id, message_id = await setup_db_standard_test_models()
    randomId = ObjectId()
    message = get_message_test(str(randomId), conver_id)
    
    response = client.post("/api/v1/message/", json=message.__dict__)

    assert response.status_code == 403
    assert response.json()['message'] == "Forbiden sender_id != user_id"

@pytest.mark.asyncio
async def test_message_send_conversation_id_not_exist_user_id_notfound() -> None:
    user_id, conver_id, message_id = await setup_db_standard_test_models()
    randomId = ObjectId()
    message = get_message_test(user_id,str(randomId))

    response = client.post("/api/v1/message/", json=message.__dict__)

    assert response.status_code == 404
    assert response.json()['message'] == f"Not found conversation with id: {str(randomId)}"

@pytest.mark.asyncio
async def test_message_send_user_id_not_belongto_conversation_forbiden() -> None:
    user_id, conver_id, message_id = await setup_db_user_not_belongto_conversation_test_models()
    randomId = ObjectId()
    message = get_message_test(user_id, conver_id)

    response = client.post("/api/v1/message/", json=message.__dict__)

    assert response.status_code == 403
    assert response.json()['message'] == f"Forbiden User ID {user_id} not belong to conversation {conver_id}"

@pytest.mark.asyncio
async def test_message_send_success() -> None:
    user_id, conver_id, message_id = await setup_db_standard_test_models()
    message = get_message_test(user_id, conver_id)
    response = client.post("/api/v1/message/", json=message.__dict__)

    assert response.status_code == 201

@pytest.mark.asyncio
async def test_message_remove_success() -> None:
    user_id, conver_id, message_id = await setup_db_standard_test_models()
    response = client.delete("/api/v1/message/" + message_id)

    assert response.status_code == 204

@pytest.mark.asyncio
async def test_message_remove_invalid_user_id_forbiden() -> None:
    user_id, conver_id, message_id = await setup_db_user_not_belongto_conversation_test_models()
    response = client.delete("/api/v1/message/" + message_id)

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_message_remove_invalid_message_id_notfound() -> None:
    user_id, conver_id, message_id = await setup_db_standard_test_models()
    randomId = ObjectId() 
    response = client.delete("/api/v1/message/" + str(randomId))

    assert response.status_code == 404

