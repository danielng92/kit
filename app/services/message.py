from app.models.messages import MessageModel
from app.repositories.manger import RepositoryManager


class MessageService():
    def __init__(self, repositories: RepositoryManager) -> None:
        self.repositories= repositories

    async def get_all(self) -> None:
        raise Exception ("This is not implemented")

    async def update(self, id: str, message: MessageModel) -> None:
        await self.repositories.message.update(message)

    async def create(self, message: MessageModel) -> None:
        await self.repositories.message.create(message)    

    async def remove(self, message: MessageModel) -> None:
        await self.repositories.message.remove(message)
    
    