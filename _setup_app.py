import trafaret as T
from trafaret_config import read_and_validate
from fastapi import FastAPI

from base.middlewares import CheckUserAuthMiddleware


def setup_app(app: FastAPI):
    """
    Настройка приложения
    """

    # Шаблон для задания структуры базы данных
    TRAFARET = T.Dict({
        T.Key('databases'): T.List(
            T.Dict({
                'name': T.String(),
                'address': T.String(),
                'collections': T.List(
                    T.Dict({
                        'name': T.String(),
                        'fields': T.List(T.String),
                        T.Key('index_fields', optional=True): T.List(T.String),
                    })
                )
            })
        )
    })

    config = read_and_validate('config.yaml', TRAFARET)
    app.config = config

    app.add_middleware(CheckUserAuthMiddleware)
