from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.models.conversations import ConversationModel, ResponseConversationModel
from app.services.manger import ServiceManager

conversations_router = APIRouter(prefix="/api/v1/conversation", tags=["Conversation"])

@conversations_router.get("/{id}")
async def get_conversation(id: str, service: ServiceManager = Depends()) -> ResponseConversationModel:
    conversation = await service.conversation.get_by_id(id)
    return conversation

@conversations_router.get("/user_id/{user_id}")
async def get_conversation(user_id: str, service: ServiceManager = Depends()) -> list[ResponseConversationModel]:
    conversations = await service.conversation.get_by_user_id(user_id)
    return conversations

@conversations_router.post("/")
async def create_conversation(conversation: ConversationModel, service: ServiceManager = Depends()) -> None:
    await service.conversation.create(conversation)
    return HTTPStatus.NO_CONTENT


@conversations_router.delete("/{id}")
async def delete_conversation(id: str, service: ServiceManager = Depends()):
    await service.conversation.remove(id)
    return HTTPStatus.NO_CONTENT