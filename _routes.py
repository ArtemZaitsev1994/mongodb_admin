from collections import namedtuple
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import RedirectResponse

from base.views import router as base_router
from base.api import router as api_router


templates = Jinja2Templates(directory="templates")


Router = namedtuple('Router', ['router', 'prefix'])

routes = [
    Router(base_router, ''),
    Router(api_router, '/api'),
]


def set_routes(app: FastAPI):
    for route in routes:
        app.include_router(
            route.router,
            prefix=route.prefix,
        )

    app.mount("/templates", StaticFiles(directory="templates"), name="templates")
    app.mount("/css", StaticFiles(directory="templates/css"), name="css")
    app.mount("/js", StaticFiles(directory="templates/js"), name="js")
    app.mount("/page_404", StaticFiles(directory="templates/errors"), name="page_404")

    @app.exception_handler(StarletteHTTPException)
    async def http_not_found_handler(request: Request, exc: Exception):
        return RedirectResponse(request.url_for('databases'))
