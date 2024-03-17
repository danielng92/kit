from fastapi import Depends
from app.common.exceptions.exceptions import NotFoundException
from app.models.conversations import ConversationModel, ResponseConversationModel
from app.repositories.manger import RepositoryManager
from app.services.base import BaseService


class ConversationService(BaseService):
    def __init__(self, repos : RepositoryManager) -> None:
        self.repos = repos

    async def create(self, conversation: ConversationModel)-> None:
        await self.repos.conversation.create(conversation)

    def update() -> None:
        raise Exception("This is not implemented")

    async def remove(self, id: str) -> None:
        message_of_conversation = await self.repos.message.get_by_conversation_id(id)
        if message_of_conversation is not None:
            for message in message_of_conversation:
                await self.repos.message.remove(message.id)
        await self.repos.conversation.remove(id)

    async def get_by_id(self, id: str) -> ResponseConversationModel:
        conversation = await self.repos.conversation.get_by_id(id)
        if conversation is None:
            raise NotFoundException(f"Not found conversation with id: {id}")
        else:
            return ResponseConversationModel(**conversation)

    async def get_by_user_id(self, user_id: str) -> list[ResponseConversationModel]:
        user = await self.repos.user.get_by_id(user_id)
        if user is None:
            raise NotFoundException(f"Not found user_id with id: {user_id}")
        return await self.repos.conversation.get_by_user_id(user_id)
    
    def get_all():
        raise Exception("This is not implemented")