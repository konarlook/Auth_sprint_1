from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from schemas.users import MixinCreateUserSchema

router = APIRouter(prefix='/auth', tags=['Auth', ])
security = HTTPBasic()


@router.get(
    path="/signup/",
    response_model=MixinCreateUserSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Регистрация пользователя',
    description='Регистрация пользователю по обязательным полям',
    tags=['Страница регистрации'],
)
async def create_user(
) -> MixinCreateUserSchema:
    """User registration endpoint by required fields."""
    # Get user email -> {if len == 0 -> next, else -> EXCEPTION]
    # Create user by email and password (and other fields)
    pass


@router.get(
    path="/login/",
    summary='Авторизация пользователя',
    description='Регистрация пользователя по логину и паролю',
    tags=['Основная страница', 'Авторизация пользователя'],
)
async def login_user():
    """User login endpoint by email and password."""
    # Get user by email -> {if len == 1 -> next, elas -> EXCEPTIOM}
    # Check is_active -> {if True -> next, elas EXCEPTION_BLOCK}
    # Check hashed password with db -> {if True -> next, else EXCEPTION_INVALID_PWD}
    # Create object history auth -> push history to DB
    # Return access and refresh tokens
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
    # Refresh JWT-token
    # Revoke both tokens to new Refresh token
    # Push old token to Redis deactivate token repository
    # Get dict with new access and refresh tokens
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
    # Refresh JWT-token
    # Revoke both tokens to new Refresh token
    # Push old token to Redis deactivate token repository
    pass


@router.get(
    path='/change_pwd/',
)
async def change_password(
        access_token: str = ...,
        old_password: str = ...,
        new_password: str = ...,
):
    """Change password from old to new."""
    # Get user by email -> always True
    # Hashed old password
    # Check hash password with db -> {if True -> next, else -> EXCEPTION}
    # Hashed new password (feature: validate password)
    # Push new password to database

    pass
