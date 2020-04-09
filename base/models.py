from typing import Dict, List, Any, Tuple

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class BaseModel:

    def __init__(self, db: AsyncIOMotorDatabase, collection: str, **kw):
        self.db = db
        self.collection = collection

    async def get_all(self, page=1, per_page=9) -> List[Dict[str, Any]]:
        all_qs = self.collection.find({})
        count_qs = await self.collection.count_documents({})
        has_next = count_qs > per_page * page
        qs = await all_qs.skip((page - 1) * per_page).limit(per_page).to_list(length=None)

        pagination = {
            'has_next': has_next,
            'prev': page - 1 if page > 1 else None,
            'next': page + 1 if has_next else None,
            'page': page,
            'per_page': per_page,
            'max': count_qs // per_page if count_qs % per_page == 0 else count_qs // per_page + 1
        }

        return qs, pagination

    async def save_item(self, data) -> Tuple[bool, str]:
        result = await self.collection.insert_one(data)
        if result:
            return True, 'was inserted new document'
        return False, "document wasn't found and wasn't inserted"

    async def update_item(self, data):
        item_id = data.pop('item_id')
        if not ObjectId.is_valid(item_id):
            return False, 'not valid id'

        _id = ObjectId(item_id)

        result = await self.collection.replace_one({'_id': _id}, data)
        if result.raw_result['updatedExisting']:
            return True, 'document updated'
        return False, 'item was not found'

    async def get_all_documents(self):
        return await self.collection.find().to_list(length=None)

    async def clear_db(self):
        await self.collection.drop()
