from typing import Dict, List, Any, Tuple

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class BaseModel:

    def __init__(self, db: AsyncIOMotorDatabase, collection: str, **kw):
        self.db = db
        self.collection = collection

    async def get_all(self, query, page=1, per_page=9) -> List[Dict[str, Any]]:
        all_qs = self.collection.find(query)
        count_qs = await self.collection.count_documents(query)
        qs = await all_qs.skip((page - 1) * per_page).limit(per_page).to_list(length=None)

        pagination = self.make_pagination(count_qs, per_page, page)
        return qs, pagination

    async def save_item(self, data) -> Tuple[bool, str]:
        result = await self.collection.insert_one(data)
        if result:
            return True, 'inserted'
        return False, 'failed'

    async def update_item(self, data) -> Tuple[bool, str]:
        item_id = data.pop('item_id')
        if not ObjectId.is_valid(item_id):
            return False, 'invalid_id'

        _id = ObjectId(item_id)

        result = await self.collection.replace_one({'_id': _id}, data)
        if result.raw_result['updatedExisting']:
            return True, 'updated'
        return True, 'inserted'

    async def remove_item(self, _id) -> Tuple[bool, str]:
        if not ObjectId.is_valid(_id):
            return False, 'invalid_id'

        _id = ObjectId(_id)
        result = await self.collection.delete_one({'_id': _id})
        if result.deleted_count == 1:
            return True, 'removed'
        return False, 'failed'

    async def get_all_documents(self) -> List[Dict[str, Any]]:
        return await self.collection.find().to_list(length=None)

    async def clear_db(self):
        await self.collection.drop()

    def make_pagination(self, count_qs, per_page, page) -> Dict[str, Any]:
        has_next = count_qs > per_page * page
        pagination = {
            'has_next': has_next,
            'prev': page - 1 if page > 1 else None,
            'next': page + 1 if has_next else None,
            'page': page,
            'per_page': per_page,
            'max': count_qs // per_page if count_qs % per_page == 0 else count_qs // per_page + 1
        }
        return pagination
