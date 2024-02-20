from fastapi import APIRouter

messages_router = APIRouter(prefix="/api/v1/message", tags=["Message"])
