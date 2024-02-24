from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.entity import CreateUserSchema

router = APIRouter()


@router.get(
    path="/signup/",
    response_model=CreateUserSchema,
    status_code=HTTPStatus.CREATED,
    summary='Регистрация пользователя',
    description='Регистрация пользователю по обязательным полям',
    tags=['Страница регистрации'],
)
async def create_user(
        user_create: CreateUserSchema,
        session: AsyncSession,
):
    """User registration endpoint by required fields."""
    pass


@router.get(
    path="/login/",
    response_model=...,
    summary='Авторизация пользователя',
    description='Регистрация пользователя по логину и паролю',
    tags=['Основная страница', 'Авторизация пользователя'],
)
async def login_user():
    """User login endpoint by email and password."""
    pass


@router.get(
    path='/refresh_token/',
    response_model=...,
    summary='Обновления refresh token',
    description='Получение новых access token и refresh token',
    tags=['Обновление токена'],
)
async def refresh_token():
    """Get new access and refresh tokens."""
    pass


@router.get(
    path='/logout/',
    response_model=...,
    summary='Выход из профиля',
    description='Выход из профиля по access token',
    tags=['Logout', ],
)
async def logout_user():
    """Logout endpoint by access token."""
    pass
