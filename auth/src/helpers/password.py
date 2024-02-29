from uuid import UUID
from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from jose import jwt
from redis.asyncio import Redis

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
beaber_scheme = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    iatime = datetime.utcnow()
    if expires_delta:
        expire = iatime + expires_delta
    else:
        expire = iatime + timedelta(minutes=30)
    to_encode.update({
        "iat": iatime,
        "exp": expire,
    })
    encoded_jwt = jwt.encode(
        to_encode,
        settings.backend.auth_secret_key,
        algorithm=settings.backend.algorithm_auth)
    return encoded_jwt


async def create_refresh_token(user_id: UUID, redis: Redis) -> str:
    refresh_token_data: dict = {"user_id": str(user_id)}
    refresh_token: str = await create_token(
        data=refresh_token_data,
        expires_delta=timedelta(days=settings.backend.auth_refresh_token_lifetime),
    )
    await redis.sadd('refresh_tokens', refresh_token)
    return refresh_token


async def create_tokens(user_id, redis) -> dict:
    access_token = await create_token(
        data={'sub': str(user_id)}
    )
    _refresh_token = await create_refresh_token(
        user_id=user_id,
        redis=redis,
    )
    return {"access_token": access_token, "refresh_token": _refresh_token}


async def decode_token(_token: str) -> dict:
    _info = jwt.get_unverified_claims(_token)
    print(_info)
    return _info


async def delete_refresh_token(refresh_token: str, redis: Redis) -> None:
    await redis.srem("refresh_tokens", refresh_token)


async def check_refresh_token(refresh_token: str, redis: Redis) -> bool:
    refresh_tokens = [refresh_token.decode('UTF-8') for refresh_token in
                      await redis.smembers('refresh_tokens')]

    if refresh_token in refresh_tokens:
        return True
    return False
