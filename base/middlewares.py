import time
import jwt

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from _settings import JWT_SECRET_KEY, JWT_ALGORITHM, AUTH_SERVER_LINK, TTL_JWT_MINUTES


class CheckUserAuthMiddleware(BaseHTTPMiddleware):
    """Миддлварь проверяет токен авторизации"""
    async def dispatch(self, request: Request, call_next, **kw):
        # проверяем только запросы к апи, тк все обращения к базе только через апи
        if not request.url.path.startswith('/api'):
            return await call_next(request)

        response = JSONResponse(
            content={
                'auth_link': AUTH_SERVER_LINK,
                'success': False,
                'invalid_token': True
            }
        )

        token = request.headers.get('Authorization')
        if not token:
            # нет токена в заголовке
            return response

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            # токен невалидный
            return response
        else:
            if payload['created_at'] + (TTL_JWT_MINUTES * 60 * 1000) < int(round(time.time() * 1000)):
                # токен устарел
                return response

        return await call_next(request)
