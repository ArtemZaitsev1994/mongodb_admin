from fastapi import FastAPI

from _routes import set_routes
from _mongo import setup_mongo
from _setup_app import setup_app


app = FastAPI()


@app.on_event('startup')
async def startup():
    setup_app(app)
    setup_mongo(app)
    set_routes(app)


@app.on_event('shutdown')
async def shutdown():
    ...
