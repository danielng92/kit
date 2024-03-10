from bson import ObjectId
from app.models.conversations import ConversationModel
from app.models.messages import MessageModel
from app.models.users import UserLoggedIn, UserModel


object_id_test = "65e33c31c943f1e991c6c8f6"

def get_mock_user_logged_in():
    return UserLoggedIn(id=object_id_test,email="test@gmail.com")

def get_user_test() -> dict:
    return {'_id': ObjectId(object_id_test),'username':"test", 'email':"test@gmail.com", 'avatar':"123",'fullname':"test",'password':"test"}

def get_conversation_test(user_id) -> ConversationModel:
    return ConversationModel(users=[user_id], latest_message="Test message", channel_name="TestChanel")

def get_message_test(user_id, conver_id) -> MessageModel:
    return MessageModel(sender_id=user_id, content="test message", conversation_id= conver_id, read_by=[user_id])