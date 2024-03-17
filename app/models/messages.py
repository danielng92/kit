from pydantic import BaseModel, Field
from typing import List

# This is message database store the content of DM or Group Chat
class MessageModel(BaseModel):
    sender_id: str
    content: str
    conversation_id: str
    read_by: List[str] #objectID list of user

class ResponseMessageModel(MessageModel):
    id: str = Field(alias="_id")
    read_by: List[dict] #objectID list of user
