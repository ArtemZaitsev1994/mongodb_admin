from typing import Dict, List

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


templates = Jinja2Templates(directory='templates')
router = APIRouter()


@router.post('/get_beer', name='get_beer')
async def get_beer(request: Request, page: int = 1, q: str = ''):
    beer, pagination = await request.app.mongo['beer'].get_all(page=page)
    for b in beer:
        b['_id'] = str(b['_id'])
    pagination['prev_link'] = request.url_for('get_beer') + f'?page={page-1}'
    pagination['next_link'] = request.url_for('get_beer') + f'?page={page+1}'
    # d = {'name': 'asd', 'rate': 50, 'manufacturer': 'a3', 'fortress': 1.2, 'gravity': 1, 'ibu': None, 'review': '', 'others': '', 'photos': {'filenames': []}}
    # await request.app.mongo['beer'].save_item(d)
    return {'beer': beer, 'pagination': pagination}


@router.get('/beer', name='beer')
async def beer(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse("admin/beer.html", context)


class Beer(BaseModel):
    name: str
    rate: int
    item_id: str = None
    manufacturer: str = ''
    fortress: float = None
    gravity: int = None
    ibu: int = None
    review: str = ''
    others: str = ''
    photos: Dict[str, List[str]] = None


@router.post('/save_beer', name='save_beer')
async def save_beer(request: Request, beer: Beer):
    beer = beer.dict()
    if beer.get('item_id'):
        return await request.app.mongo['beer'].update_item(beer)
    return await request.app.mongo['beer'].save_item(beer)
