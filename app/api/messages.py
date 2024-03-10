from fastapi import APIRouter, Depends, status
from app.api.auth import get_current_user
from app.common.exceptions.exceptions import ForbidenException
from app.models.messages import MessageModel
from app.models.users import UserLoggedIn

from app.services.manger import ServiceManager
from app.utils.conver_mongo_data import convert_message_to_mongo_data, convert_message_to_py_data

messages_router = APIRouter(prefix="/api/v1/message", tags=["Message"])
@messages_router.get("/{id}")
async def get_message(id:str, services: ServiceManager = Depends()):
    return await services.message.get_by_id(id)

@messages_router.post("/", status_code=status.HTTP_201_CREATED)
async def send_message(message: MessageModel, services: ServiceManager = Depends(), user: UserLoggedIn = Depends(get_current_user)):
    if user.id != message.sender_id:
        raise ForbidenException("sender_id != user_id")
    conversation = await services.conversation.get_by_id(message.conversation_id)
    #Todo optimize how to get users id in conversation
    list_user_id_of_conversation: list[str] = (u['_id'] for u in conversation.users)
    if user.id not in list_user_id_of_conversation:
        raise ForbidenException(f"User ID {user.id} not belong to conversation {conversation.id}")
    await services.message.create(message)
    return ""

@messages_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def send_message(id: str, services: ServiceManager = Depends(), user: UserLoggedIn = Depends(get_current_user)):
    message = await services.message.get_by_id(id)
    if user.id != message.sender_id:
        raise ForbidenException()
    await services.message.remove(message.id)
    return ""

@messages_router.get("/")
async def get_by_conversation_id(conversation_id: str, services: ServiceManager = Depends(), user: UserLoggedIn = Depends(get_current_user)):
    conversation = await services.conversation.get_by_id(conversation_id)
    list_user_id_of_conversation = (u['_id'] for u in conversation.users)
    if user.id not in list_user_id_of_conversation:
        raise ForbidenException()
    return await services.message.get_by_conversation_id(conversation_id)

@messages_router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_message(id: str, message_content: str, services: ServiceManager = Depends(), user: UserLoggedIn = Depends(get_current_user)):
    message_db = await services.message.get_by_id(id)
    print(message_db)
    if user.id != message_db.sender_id:
        raise ForbidenException()
    message_db.content = message_content
    await services.message.update(id, convert_message_to_py_data(message_db))
    return ""