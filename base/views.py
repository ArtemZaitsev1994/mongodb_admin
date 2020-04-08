from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates')
router = APIRouter()


@router.get('/contacts', name='contacts')
async def contacts(request: Request):
    return templates.TemplateResponse('contacts/contacts.html', {'request': request})
