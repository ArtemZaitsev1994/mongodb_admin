import os

import trafaret as T
from trafaret_config import read_and_validate
from fastapi import FastAPI
from envparse import env


# beerblog mongo collection's name
BEER_BLOG_COLLECTION = 'bb_beer'

if os.path.isfile('.env'):
    env.read_envfile('.env')

    MONGO_HOST = env.str('MONGO_HOST')
    MONGO_DB_BEER_BLOG = env.str('MONGO_DB_BEER_BLOG')

    MONGO_ADMIN_LOGIN = env.str('MONGO_ADMIN_LOGIN')
    MONGO_ADMIN_PASSWORD = env.str('MONGO_ADMIN_PASSWORD')
else:
    raise SystemExit('Create an env-file please.!')


def setup_app(app: FastAPI):
    TRAFARET = T.Dict({
        T.Key('databases'): T.List(
            T.Dict({
                'name': T.String(),
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
    # BASEDIR = os.path.dirname(os.path.realpath(__file__))
    # PHOTO_PATH = os.path.join(BASEDIR, 'static/photo/')

    # app.beer_photo_path = os.path.join(PHOTO_PATH, 'beer')
