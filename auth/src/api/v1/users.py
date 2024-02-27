from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from schemas.users import (CreateUserSchema,
                           UserBaseSchema,
                           LoginUserResponseSchema,
                           LoginUserSchema,
                           LoginUserResponseSchema,
                           )
from services.user_service import AuthUserService, get_user_service
from helpers.exceptions import AuthException
from helpers.password import verify_password, create_access_token

router = APIRouter(prefix='/auth', tags=['Auth', ])
security = HTTPBasic()


@router.get(
    path="/signup/",
    response_model=UserBaseSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Регистрация пользователя',
    description='Регистрация пользователя по обязательным полям',
    tags=['Страница регистрации'],
)
async def create_user(
        user_dto: CreateUserSchema = Depends(),
        user_service: AuthUserService = Depends(get_user_service)
) -> UserBaseSchema:
    """User registration endpoint by required fields."""
    request_email = await user_service.get(email=user_dto.email)
    if request_email:
        raise AuthException(
            message="User already exists",
            status_code=status.HTTP_409_CONFLICT,
        )
    user = await user_service.create(user_dto=user_dto)
    return user


@router.get(
    path="/login/",
    response_model=LoginUserResponseSchema,
    summary='Авторизация пользователя',
    description='Регистрация пользователя по логину и паролю',
    tags=['Основная страница', 'Авторизация пользователя'],
)
async def login_user(
        user_dto: LoginUserSchema = Depends(),
        user_service: AuthUserService = Depends(get_user_service),
) -> LoginUserResponseSchema:
    """User login endpoint by email and password."""
    request_email = await user_service.get(email=user_dto.email)
    if not request_email:
        raise AuthException(
            message="Incorrect email or password.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if not verify_password(
            user_dto.hashed_password,
            request_email.hashed_password,
    ):
        raise AuthException(
            message="Incorrect email or password.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    access_token = create_access_token(
        data={'sub': request_email.email}
    )
    return LoginUserResponseSchema(access_token=access_token, refresh_token='12')
    # Create object history auth -> push history to DB

    # Return access and refresh tokens


@router.get(
    path='/refresh_token/',
    summary='Обновления refresh token',
    description='Получение новых access token и refresh token',
    tags=['Обновление токена'],
)
async def refresh_token(
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

):
    """Change password from old to new."""
    # Get user by email -> always True
    # Hashed old password
    # Check hash password with db -> {if True -> next, else -> EXCEPTION}
    # Hashed new password (feature: validate password)
    # Push new password to database

    pass
