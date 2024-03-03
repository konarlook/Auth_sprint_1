import functools
from datetime import datetime
import jwt
from fastapi import HTTPException, status
from core.config import settings


async def is_token_expired(token: str) -> bool:
    if token:
        token_info: dict = jwt.decode(
            jwt=token,
            key=settings.auth_jwt.public_key.read_text(),
            algorithms=[settings.auth_jwt.auth_algorithm_password, ]
        )
        token_expired = datetime.utcfromtimestamp(token_info.get("exp"))

        if token_expired > datetime.utcnow():
            return True
    return False


def check_access_token(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        access_token = kwargs.get('access_token')
        if not await is_token_expired(access_token):
            raise HTTPException(
                detail='Incorrect access token.',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return await func(*args, **kwargs)

    return wrapper
