import bson
from motor.motor_asyncio import AsyncIOMotorCursor

def serialize_dict(doc) -> dict | None:
    if isinstance(doc, dict):
        serialized = {
            "_id": str(doc["_id"]),  # Convert ObjectId to string (assuming it's in the root dict)
            **{
                i: serialize_dict(v) if isinstance(v, (dict, list)) 
                else str(v) if isinstance(v, bson.ObjectId) 
                else v for i, v in doc.items() if i != "_id"
            } 
        }
    elif isinstance(doc, list):
        serialized = [serialize_dict(item) for item in doc]  # Serialize each item in the list
    elif isinstance(doc, bson.ObjectId):
        serialized = {"_id": str(doc)} # Convert ObejctId to string if not populate
    else:
        serialized = doc  # Pass through other types as-is
    return serialized

async def serialize_list(cursor: AsyncIOMotorCursor) -> list | None:
    docs = await cursor.to_list(None)
    if(len(docs) == 0):
        return None
    return [serialize_dict(doc) for doc in docs]