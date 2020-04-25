import json
import asyncio
import jwt
from typing import Dict, Any
from functools import partial
from urllib.request import Request, urlopen
from _settings import JWT_SECRET_KEY, JWT_ALGORITHM


async def send_reqeuest(url: str, method: str = 'GET', data: Dict[str, Any] = None) -> Dict[str, Any]:
    data = json.dumps(data)

    req = Request(url, data=bytes(data.encode("utf-8")), method="POST")
    req.add_header("Content-type", "application/json; charset=UTF-8")

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(urlopen, req))


def decode_jwt(token):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
