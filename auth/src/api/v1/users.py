from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get(
    path="/register/",
    response_model=...,
    summary='Регистрация пользователя',
    description='Регистрация пользователю по обязательным полям',
    tags=['Страница регистрации'],
)
async def register_user():
    pass


@router.get(
    path="/login/",
    response_model=...,
    summary='Авторизация пользователя',
    description='Регистрация пользователя по логину и паролю',
    tags=['Основная страница', 'Авторизация пользователя'],
)
async def login_user():
    pass


@router.get(
    path='/refresh_token/',
    response_model=...,
    summary='Обновления refresh token',
    description='Получение новых access token и refresh token',
    tags=['Обновление токена'],
)
async def refresh_token():
    pass


@router.get(
    path='/logout/',
    response_model=...,
    summary='Выход из профиля',
    description='Выход из профиля по access token',
    tags=['Logout',],
)
async def logout_user():
    pass
