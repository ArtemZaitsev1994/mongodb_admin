from typing import Dict, Any, List

from fastapi import APIRouter, Request
from pydantic import BaseModel
from pymongo import errors

from _settings import AUTH_SERVER_LINK


router = APIRouter()


class DataIn(BaseModel):
    db: str
    collection: str
    page: int = 1
    fields_filter: List[Any] = []
    text: str = ''


class BaseResponse(BaseModel):
    success: bool
    message: str = ''
    item_fields: List = None
    items: List[Dict[str, Any]] = None
    pagination: Dict[str, Any] = None


@router.post('/get_data', name='get_data')
async def get_data(request: Request, data: DataIn, response_model=BaseResponse):
    """Получение данных из базы"""
    page = data.page
    query = {}

    # выбранные поля заполнены
    # TODO: переделать
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

    # полнотекстовой поиск
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
    pagination['prev_link'] = f'{request.url_for("get_data")}?page={page-1}'
    pagination['next_link'] = f'{request.url_for("get_data")}?page={page+1}'

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


@router.post('/get_dbs', name='get_dbs')
async def get_dbs(request: Request):
    dbs = request.app.mongo
    response = {
        'dbs': [{'name': x, 'collections': list(dbs[x].keys())} for x in dbs],
        'success': True
    }
    return response


@router.post('/get_auth_link', name='get_auth_link', tags=['trusted'])
async def get_auth_link(request: Request):
    response = {
        'link': AUTH_SERVER_LINK,
        'success': True
    }
    return response


@router.post('/check_token', name='check_token', tags=['trusted'])
async def check_token(request: Request, token: Dict[str, str]):
    """Заглушка для проверки токена, токен проверится в миддлвари"""
    return {'success': True}
