import asyncio
from functools import wraps
import json
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.common.exceptions.exceptions import UnauthorizeException

async def validate_token(request: Request):
    try:
        token = await oauth2_scheme(request)
        if not token:
            raise UnauthorizeException("Unauthorized"  + str(error))
    except OAuthError as error:
        raise UnauthorizeException("Unauthorized"  + str(error))

# Authorization decorator
def authorize(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print("in wrapper")
        for arg_name, arg_value in kwargs.items():
            if isinstance(arg_value, Request):
                print("unauthorized")
                await validate_token(arg_value)
                print("authorized")
        return await func(*args, **kwargs)
    return wrapper

# Class-level authorization decorator
def authorize_class(cls):
    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, authorize(method) if asyncio.iscoroutinefunction(method) else method)
    return cls

config = Config('./app/.env')
oauth = OAuth(config)
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    },
    authorize_state = 'lQZeeEEnXUeceKeRyocInMIVDaOV0q'
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
)

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@auth_router.get('/')
async def homepage(request: Request, token: str = Depends(oauth2_scheme)):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        return JSONResponse(status_code=200, content={'user': str(data)})
    return {"Success!"}


@auth_router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_router.get('/callback')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>ERROR: {error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='http://127.0.0.1:8000/docs')


@auth_router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')
