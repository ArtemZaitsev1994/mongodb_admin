from typing import Dict, Any, List

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pymongo import errors


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


class BaseResponse(BaseModel):
    success: bool
    message: str = ''
    item_fields: List = None
    items: List[Dict[str, Any]] = None
    pagination: Dict[str, Any] = None


@router.post('/get_data', name='get_data')
async def get_data(request: Request, data: DataIn, response_model=BaseResponse):
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

    try:
        items, pagination = await request.app.mongo[data.db][data.collection].db\
            .get_all(query, page=page)
    except errors.OperationFailure:
        response = {
            'success': False,
            'message': 'error accessing mongo',
        }
        return response

    for item in items:
        item['_id'] = str(item['_id'])
    pagination['prev_link'] = request.url_for('get_beer') + f'?page={page-1}'
    pagination['next_link'] = request.url_for('get_beer') + f'?page={page+1}'

    response = {
        'success': True,
        'item_fields': request.app.mongo[data.db][data.collection].fields,
        'items': items,
        'pagination': pagination,
    }
    return response


@router.post('/save_item', name='save_item', response_model=BaseResponse)
async def save_item(request: Request, item: Dict[str, Any]):
    if item.get('item_id'):
        success, message = await request.app.mongo[item['db']][item['collection']]\
            .db.update_item(item)
    else:
        success, message = await request.app.mongo[item['db']][item['collection']]\
            .db.save_item(item)

    response = {
        'success': success,
        'message': message
    }

    return response


@router.post('/remove_item', name='remove_item', response_model=BaseResponse)
async def remove_item(request: Request, item: Dict[str, Any]):
    success, message = await request.app.mongo[item['db']][item['collection']]\
        .db.remove_item(item['_id'])
    response = {
        'success': success,
        'message': message
    }

    return response


# @router.post('/save_item', name='save_item')
# async def save_item(request: Request, **kwargs: Dict):
#     return await request.app.mongo['beer'].save_item(kwargs)
