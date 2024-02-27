from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

from core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
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
