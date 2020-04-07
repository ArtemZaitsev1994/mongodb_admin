from aioredis import Redis
from aiohttp import web
from aiohttp.web import middleware
from aiohttp_session import get_session


@middleware
async def authorize(request, handler):
    def check_path(path):
        """Проверка разрешен ли путь"""
        paths = ['/admin', ]
        for r in paths:
            if path.startswith(r):
                return False
        return True

    async def check_token(redis: Redis, token: str) -> bool:
        return await redis.get(token)

    if check_path(request.path):
        return await handler(request)

    session = await get_session(request)
    if session.get('admin_token'):
        if await check_token(request.app['redis'], session['admin_token']):
            return await handler(request)

    url = request.app.router['login'].url_for()
    raise web.HTTPFound(url)
