from motor import motor_asyncio as ma
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.applications import FastAPI

from _settings import MONGO_DB_BEER_BLOG, MONGO_HOST
from beerblog.models import Beer
from base.models import BaseModel


def setup_mongo(app: FastAPI):
    app.client = ma.AsyncIOMotorClient(MONGO_HOST)
    app.mongo = {}

    for db in app.config['databases']:
        app.mongo[db['name']] = {}
        for collection in db['collections']:
            print(collection['fields'])
            app.mongo[db['name']][collection['name']] = (
                BaseModel(app.client[db['name']], collection['name']),
                collection['fields']
            )
