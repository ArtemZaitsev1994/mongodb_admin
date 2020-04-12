from typing import Dict, Any, List

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
    fields_filter: List = []
    text: str = ''


@router.post('/get_data', name='get_data')
async def get_data(request: Request, data: DataIn):
    page = data.page
    query = {}

    if data.fields_filter:
        query = dict(
            zip(
                data.fields_filter, [
                    {"$nin": ['', -1, None], "$exists": True}
                    for x
                    in data.fields_filter
                ]
            )
        )

    if data.text:
        query['$text'] = {'$search': data.text}

    items, pagination = await request.app.mongo[data.db][data.collection].db\
        .get_all(query, page=page)

    for item in items:
        item['_id'] = str(item['_id'])
    pagination['prev_link'] = request.url_for('get_beer') + f'?page={page-1}'
    pagination['next_link'] = request.url_for('get_beer') + f'?page={page+1}'

    response = {
        'fields': request.app.mongo[data.db][data.collection].fields,
        'items': items,
        'pagination': pagination,
    }
    return response


@router.post('/save_item', name='save_item')
async def save_item(request: Request, item: Dict[str, Any]):
    if item.get('item_id'):
        return await request.app.mongo[item['db']][item['collection']].db.update_item(item)
    return await request.app.mongo[item['db']][item['collection']].db.save_item(item)


# @router.post('/save_item', name='save_item')
# async def save_item(request: Request, **kwargs: Dict):
#     return await request.app.mongo['beer'].save_item(kwargs)
