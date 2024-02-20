from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.repositories.manger import RepositoryManager
from app.models.conversations import ConversationModel, ResponseConversationModel

conversations_router = APIRouter(prefix="/api/v1/conversation", tags=["Conversation"])

@conversations_router.get("/{id}")
async def get_conversation(id: str, repositories: RepositoryManager = Depends()) -> dict:
    conversation = await repositories.conversation.get_by_id(id)
    return conversation

@conversations_router.get("/all-info/{id}")
async def get_conversation_all_info(id: str, repositories: RepositoryManager = Depends()) -> dict:
    conversation = await repositories.conversation.get_by_id_all_info(id)
    return conversation

@conversations_router.get("/")
async def get_conversations(repositories: RepositoryManager = Depends()) -> list[ResponseConversationModel]:
    conversations = await repositories.conversation.get_all()
    return conversations

@conversations_router.post("/")
async def create_conversation(conversation: ConversationModel, repositories: RepositoryManager = Depends()):
    await repositories.conversation.create(conversation)
    return HTTPStatus.NO_CONTENT

@conversations_router.put("/{id}")
async def update_conversation(id: str, conversation: ConversationModel, repositories: RepositoryManager =Depends()):
    await repositories.conversation.update(id, conversation)
    return HTTPStatus.NO_CONTENT

@conversations_router.delete("/{id}")
async def delete_conversation(id: str, repositories: RepositoryManager = Depends()):
    await repositories.conversation.remove(id)
    return HTTPStatus.NO_CONTENT