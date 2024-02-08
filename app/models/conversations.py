from pydantic import BaseModel, Field
from typing import List, Optional

class ConversationModel(BaseModel):
    is_channel: bool = False 
    users: List[str]
    group_admin: Optional[str] = None
    channel_name: str
    latest_message: str

class ResponseConversationModel(BaseModel):
    id: str = Field(alias="_id")
    is_channel: bool = False 
    users: List[dict]
    group_admin: Optional[str] = None
    channel_name: str
    latest_message: str

