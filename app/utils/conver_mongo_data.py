from bson import ObjectId
from app.models.conversations import ConversationModel
from app.models.messages import MessageModel, ResponseMessageModel

def convert_conversations_to_mongo_data(conversation: ConversationModel) -> dict:
  doc = {
      "is_channel": conversation.is_channel,
      "users": [ObjectId(user_id) for user_id in conversation.users],
      "group_admin": ObjectId(conversation.group_admin),
      "latest_message": conversation.latest_message,
      "channel_name": conversation.channel_name
    }
  return doc

def convert_message_to_mongo_data(message: MessageModel) -> dict:
  doc = {
    "sender_id": ObjectId(message.sender_id),
    "content": message.content,
    "conversation_id": ObjectId(message.conversation_id),
    "read_by": [ObjectId(user_id) for user_id in message.read_by],
  }
  return doc

def convert_message_to_py_data(message: ResponseMessageModel) -> MessageModel:
  return MessageModel(
    sender_id=str(message.sender_id), 
    content=message.content, 
    conversation_id=str(message.conversation_id), 
    read_by= [str(item['_id']) for item in message.read_by]
  )
