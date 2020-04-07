from fastapi import FastAPI

from _routes import set_routes
from _mongo import setup_mongo
from _settings import setup_app


app = FastAPI()

setup_app(app)
setup_mongo(app)
set_routes(app)
