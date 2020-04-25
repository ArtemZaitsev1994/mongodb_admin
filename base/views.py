import time

import jwt
from starlette.responses import RedirectResponse
from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates

from _settings import JWT_SECRET_KEY, JWT_ALGORITHM, AUTH_SERVER_LINK, TTL_JWT_MINUTES


templates = Jinja2Templates(directory='templates')
router = APIRouter()


@router.get('/contacts', name='contacts')
async def contacts(request: Request):
    return templates.TemplateResponse('contacts/contacts.html', {'request': request})


@router.get('/databases', name='databases')
async def databases(request: Request):
    context = {
        'request': request
    }
    return templates.TemplateResponse('admin/databases.html', context)


@router.get('/auth/{token}', name='auth', tags=['trusted'])
async def auth(response: Response, request: Request, token: str):
    """Метод для принятия авторизации"""
    # TODO: ExpiredSignatureError
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return RedirectResponse(AUTH_SERVER_LINK)
    else:
        if payload['created_at'] + (TTL_JWT_MINUTES * 60 * 1000) < int(round(time.time() * 1000)):
            return RedirectResponse(AUTH_SERVER_LINK)

    response = RedirectResponse(request.url_for('databases'))
    response.set_cookie(key='Authorization', value=token)
    return response
