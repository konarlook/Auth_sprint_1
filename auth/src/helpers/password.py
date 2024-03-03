from uuid import UUID, uuid4
from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from jose import jwt
from redis.asyncio import Redis
from redis.exceptions import DataError


from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
beaber_scheme = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def create_token(data: dict,
                       client_id: str,
                       expires_delta: timedelta | None = None) -> str:
    """Function for creating access token."""
    to_encode = data.copy()
    iatime = datetime.utcnow()

    if expires_delta:
        expire = iatime + expires_delta
    else:
        expire = iatime + timedelta(minutes=30)
    to_encode.update({
        "iat": iatime,
        "exp": expire,
        'client_id': str(client_id),
        'jti': str(uuid4()),
    })
    encoded_jwt = jwt.encode(
        to_encode,
        settings.backend.auth_secret_key,
        algorithm=settings.backend.auth_algorithm_password)
    return encoded_jwt


async def create_access_token(data: dict, actions: str, client_id: str):
    """Function for creating access token."""
    access_token_data = {
        'sub': str(data['id']),
        'actions': actions,
    }
    access_token = await create_token(
        data=access_token_data,
        client_id=client_id,
    )
    return access_token


async def create_refresh_token(_id: UUID, client_id: str, redis: Redis) -> str:
    """Function for creating refresh token."""
    refresh_token_data: dict = {"id": str(_id)}
    refresh_token: str = await create_token(
        data=refresh_token_data,
        client_id=client_id,
        expires_delta=timedelta(days=settings.backend.auth_refresh_token_lifetime),
    )
    await redis.sadd('refresh_tokens', refresh_token)
    return refresh_token


async def create_tokens(data: dict, *, client_id: str, actions: str, redis) -> dict:
    _access_token = await create_access_token(
        data=data,
        actions=actions,
        client_id=client_id
    )
    _refresh_token = await create_refresh_token(
        _id=data['id'],
        client_id=client_id,
        redis=redis,
    )
    return {"access_token": _access_token, "refresh_token": _refresh_token}


async def decode_token(_token: str) -> dict:
    _info = jwt.get_unverified_claims(_token)
    return _info


async def delete_refresh_token(refresh_token: str, redis: Redis) -> bool:
    try:
        await redis.srem("refresh_tokens", refresh_token)
        return True
    except DataError:
        return False


async def check_refresh_token(refresh_token: str, redis: Redis) -> bool:
    refresh_tokens = [refresh_token.decode('UTF-8') for refresh_token in
                      await redis.smembers('refresh_tokens')]

    if refresh_token in refresh_tokens:
        return True
    return False
