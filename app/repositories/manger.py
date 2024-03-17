from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from app.config.mongodb import get_db
from app.repositories.message import MessageRepository
from app.repositories.user import UserRepository
from app.repositories.conversation import ConversationRepository
from app.repositories.message import MessageRepository


class RepositoryManager:
    _db: AsyncIOMotorDatabase
    _user: UserRepository
    _conversation: ConversationRepository
    _message: MessageRepository

    def __init__(self, db: Annotated[AsyncIOMotorDatabase,Depends(get_db)]) -> None:
        self._db = db
        self._user = None
        self._conversation = None
        self._message = None

    @property
    def user(self) -> UserRepository:
        if(self._user is None):
            self._user = UserRepository(self._db["users"])
        return self._user
    
    @property
    def conversation(self) -> ConversationRepository:
        if(self._conversation is None):
            self._conversation = ConversationRepository(self._db["conversations"])
        return self._conversation
    
    @property
    def message(self) -> MessageRepository:
        if(self._message is None):
            self._message = MessageRepository(self._db["messages"])
        return self._message