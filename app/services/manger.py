from app.services.conversation import ConversationService
from app.services.message import MessageService
from app.services.user import UserService
from app.repositories.manger import RepositoryManager
from typing import Annotated
from fastapi import Depends
class ServiceManager:
    _repo: RepositoryManager
    _user: UserService
    _conversation: ConversationService
    _message: MessageService

    def __init__(self, repo: RepositoryManager = Depends()) -> None:
        self._repo = repo
        self._user = None
        self._conversation = None
        self._message = None

    @property
    def user(self) -> UserService:
        if(self._user is None):
            self._user = UserService(self._repo)
        return self._user
    
    @property
    def conversation(self) -> ConversationService:
        if(self._conversation is None):
            self._conversation = ConversationService(self._repo)
        return self._conversation
    
    @property
    def message(self) -> MessageService:
        if(self._message is None):
            self._message = MessageService(self._repo)
        return self._message
    