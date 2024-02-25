from typing import Annotated
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.entity import CreateUserSchema

router = APIRouter(prefix='/auth', tags=['Auth', ])
security = HTTPBasic()


@router.get(
    path="/signup/",
    summary='Регистрация пользователя',
    description='Регистрация пользователю по обязательным полям',
    tags=['Страница регистрации'],
)
async def create_user(
        user_create: CreateUserSchema
) -> dict[str]:
    """User registration endpoint by required fields."""
    if username in database:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )


@router.get(
    path="/login/",
    summary='Авторизация пользователя',
    description='Регистрация пользователя по логину и паролю',
    tags=['Основная страница', 'Авторизация пользователя'],
)
async def login_user():
    """User login endpoint by email and password."""
    pass


@router.get(
    path='/refresh_token/',
    summary='Обновления refresh token',
    description='Получение новых access token и refresh token',
    tags=['Обновление токена'],
)
async def refresh_token(
        username: str = Depends(...)
) -> dict[str, str]:
    """Get new access and refresh tokens."""
    pass


@router.get(
    path='/logout/',
    summary='Выход из профиля',
    description='Выход из профиля по access token',
    tags=['Logout', ],
)
async def logout_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    """Logout endpoint by access token."""
    pass


@router.get(
    path='/change_pwd/',
)
async def change_password(
        access_token: str = ...,
        old_password: str = ...,
        new_password: str = ...,
):
    pass
