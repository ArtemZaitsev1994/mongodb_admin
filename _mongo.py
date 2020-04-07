from motor import motor_asyncio as ma
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.applications import FastAPI

from _settings import MONGO_DB_BEER_BLOG, MONGO_HOST
from beerblog.models import Beer


def setup_mongo(app: FastAPI):
    app.client = ma.AsyncIOMotorClient(MONGO_HOST)
    app.db_beer = app.client[MONGO_DB_BEER_BLOG]

    app.mongo = {
        'beer': Beer(app.db_beer)
    }
