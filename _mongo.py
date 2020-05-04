from collections import namedtuple
from motor import motor_asyncio as ma
from fastapi.applications import FastAPI

from _settings import MONGO_HOST
from base.models import BaseModel


MongoInstance = namedtuple('MongoInstance', ['db', 'fields', 'index_fields'])


class WrongCollectionFormat(Exception):
    def __init__(self, text):
        self.txt = text


def setup_mongo(app: FastAPI):
    """
    Создаем инстанс Монги
    """
    # app.client = ma.AsyncIOMotorClient(MONGO_HOST)
    app.mongo = {}

    for db in app.config['databases']:
        client = ma.AsyncIOMotorClient(db['address'])
        app.mongo[db['name']] = {}

        for collection in db['collections']:
            index_fields = collection.get('index_fields')
            if index_fields:
                if len(list(set(collection['index_fields']) - set(collection['fields']))) > 0:
                    raise WrongCollectionFormat('"index_fields" got an extra fields not included in "fields"')

            db_instance = client[db['name']]
            collection_instance = db_instance[collection['name']]

            app.mongo[db['name']][collection['name']] = MongoInstance(
                BaseModel(db_instance, collection_instance),
                collection['fields'],
                index_fields,
            )
