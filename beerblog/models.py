from motor.motor_asyncio import AsyncIOMotorDatabase

from base.models import BaseModel
from _settings import BEER_BLOG_COLLECTION


class Beer(BaseModel):
    def __init__(self, db: AsyncIOMotorDatabase, **kw):
        super().__init__(db)
        self.collection = self.db[BEER_BLOG_COLLECTION]
