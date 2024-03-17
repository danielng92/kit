from app.common.exceptions.exceptions import NotFoundException
from app.models.messages import MessageModel, ResponseMessageModel
from app.repositories.manger import RepositoryManager


class MessageService():
    def __init__(self, repositories: RepositoryManager) -> None:
        self.repositories= repositories

    async def get_all(self) -> None:
        raise Exception ("This is not implemented")
    
    async def get_by_id(self, id: str) -> ResponseMessageModel:
        message = await self.repositories.message.get_by_id(id)
        if message is None:
            raise NotFoundException(f"Not found message with this id: {id}")
        return ResponseMessageModel(**message)
    
    async def update(self, id:str , message: MessageModel) -> None:
        user =await self.repositories.user.get_by_id(message.sender_id)
        if user is None:
            raise NotFoundException(f"Not found user with this id: {message.sender_id}")
        await self.repositories.message.update(id ,message)

    async def create(self, message: MessageModel) -> None:
        user =await self.repositories.user.get_by_id(message.sender_id)
        if user is None:
            raise NotFoundException(f"Not found user with this id: {message.sender_id}")
        await self.repositories.message.create(message)    

    async def remove(self, message: MessageModel) -> None:
        await self.repositories.message.remove(message)
    
    async def get_by_conversation_id(self, conversation_id: str) -> list[MessageModel]:
        conversation= await self.repositories.conversation.get_by_id(conversation_id)
        if conversation is None:
            raise NotFoundException(f"Not found conversation with this id: {conversation_id}")
        return await self.repositories.message.get_by_conversation_id(conversation_id)
        
    async def check_sender_id_exists(self, sender_id: str):
        user =await self.repositories.user.get_by_id(sender_id)
        if user is None:
            raise NotFoundException(f"Not found user with this id: {sender_id}")