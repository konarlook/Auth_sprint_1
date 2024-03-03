import functools
from datetime import datetime
from fastapi import HTTPException, status
from .password import decode_token


async def is_token_expired(token: str) -> bool:
    if token:
        token_info: dict = await decode_token(token)
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
