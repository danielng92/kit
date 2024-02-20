from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.users import user_router
from app.api.conversations import conversations_router
from app.api.messages import messages_router
from app.common.exceptions.bad_request import BadRequestException
from app.common.exceptions.not_found import NotFoundException

app = FastAPI()
app.include_router(user_router)
app.include_router(conversations_router)
app.include_router(messages_router)

@app.middleware("http")
async def handle_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except NotFoundException as exc:
        return JSONResponse(status_code=404, content={'message': str(exc)})
    except BadRequestException as exc:
        return JSONResponse(status_code=400, content={'message': str(exc)})
    except Exception as exc:
        return JSONResponse(status_code=500, content={'message': str(exc)})    