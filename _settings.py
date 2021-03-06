import os
from envparse import env


# beerblog mongo collection's name
BEER_BLOG_COLLECTION = 'bb_beer'

if os.path.isfile('.env'):
    env.read_envfile('.env')
else:
    raise SystemExit('Create an env-file please.!')

JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
JWT_ALGORITHM = env.str('JWT_ALGORITHM')
AUTH_SERVER_LINK = env.str('AUTH_SERVER_LINK')
TTL_JWT_MINUTES = env.int('TTL_JWT_MINUTES')
