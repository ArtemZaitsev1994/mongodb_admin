from typing import Dict, Any

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
    page: int = 1


@router.post('/get_data', name='get_data')
async def get_data(request: Request, data: DataIn):
    page = data.page
    items, pagination = await request.app.mongo[data.db][data.collection][0].get_all(page=page)
    for item in items:
        item['_id'] = str(item['_id'])
    pagination['prev_link'] = request.url_for('get_beer') + f'?page={page-1}'
    pagination['next_link'] = request.url_for('get_beer') + f'?page={page+1}'

    response = {
        'fields': request.app.mongo[data.db][data.collection][1],
        'items': items,
        'pagination': pagination,
    }
    return response


@router.post('/save_item', name='save_item')
async def save_item(request: Request, item: Dict[str, Any]):
    if item.get('item_id'):
        return await request.app.mongo[item['db']][item['collection']][0].update_item(item)
    return await request.app.mongo[item['db']][item['collection']][0].save_item(item)


# @router.post('/save_item', name='save_item')
# async def save_item(request: Request, **kwargs: Dict):
#     return await request.app.mongo['beer'].save_item(kwargs)
