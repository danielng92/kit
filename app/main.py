from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.api.users import user_router
from app.api.conversations import conversations_router
from app.api.auth import auth_router, oauth
from app.api.messages import messages_router
from app.common.exceptions.bad_request import BadRequestException
from app.common.exceptions.exceptions import UnauthorizeException
from app.common.exceptions.not_found import NotFoundException

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='!secret', https_only=False)

@app.middleware("http")
async def validate_token(request: Request, call_next):
    if "api/v1" not in request.url.path or "api/v1/auth" in request.url.path:
        return await call_next(request)
    response = await call_next(request)
    try:
        user = request.session.get('user')
        if user is None:
            raise UnauthorizeException("Unauthorized")
    except Exception as error:
        raise UnauthorizeException("Unauthorized "  + str(error))
    return response

@app.middleware("http")
async def handle_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except NotFoundException as exc:
        return JSONResponse(status_code=404, content={'message': str(exc)})
    except BadRequestException as exc:
        return JSONResponse(status_code=400, content={'message': str(exc)})
    except UnauthorizeException as exc:
        return JSONResponse(status_code=401, content={'message': str(exc)})
    except Exception as exc:
        return JSONResponse(status_code=500, content={'message': str(exc)})    
    
app.include_router(user_router)
app.include_router(conversations_router)
app.include_router(messages_router)
app.include_router(auth_router)