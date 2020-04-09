from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


templates = Jinja2Templates(directory='templates')
router = APIRouter()


@router.get('/contacts', name='contacts')
async def contacts(request: Request):
    return templates.TemplateResponse('contacts/contacts.html', {'request': request})


@router.get('/databases', name='databases')
async def databases(request: Request):
    context = {
        'request': request,
        'dbs': request.app.mongo
    }
    return templates.TemplateResponse('admin/databases.html', context)


class DataIn(BaseModel):
    db: str
    collection: str


@router.post('/get_data', name='get_data')
async def get_data(request: Request, data: DataIn):
    response = {
        'fields': request.app.mongo[data.db][data.collection][1]
    }
    return response
