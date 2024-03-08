from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import JSONResponse
from app.config.settings import Settings
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.common.exceptions.exceptions import UnauthorizeException

settings = Settings()
uri = settings.MONGODB_CONNECT_STRING
config = Config('./app/.env')
oauth = OAuth(config)
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    },
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
)

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@auth_router.get('/me')
async def homepage(request: Request):
    user = request.session.get('user')
    print(user)
    return user


@auth_router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_router.get('/callback')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/docs')


@auth_router.get('/logout')
def logout(request: Request):
    request.session.pop('user')
    request.session.clear()
    return RedirectResponse('/docs')
