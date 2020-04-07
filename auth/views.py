import secrets

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from _settings import MONGO_ADMIN_LOGIN, MONGO_ADMIN_PASSWORD


security = HTTPBasic()
router = APIRouter()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, MONGO_ADMIN_LOGIN)
    correct_password = secrets.compare_digest(credentials.password, MONGO_ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/", name='auth')
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}

