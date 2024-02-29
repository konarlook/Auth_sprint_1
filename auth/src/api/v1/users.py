from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasic
from redis.asyncio import Redis

from schemas.users import (CreateUserSchema,
                           UserBaseSchema,
                           LoginUserResponseSchema,
                           LoginUserSchema,
                           LoginUserResponseSchema,
                           MainInfoUserSchema,
                           RefreshTokenUserSchema,
                           ChangePasswordSchema)
from services.user_service import AuthUserService, get_user_service
from helpers.exceptions import AuthException
from helpers.password import (verify_password,
                              create_token,
                              create_refresh_token,
                              check_refresh_token,
                              create_tokens,
                              delete_refresh_token,
                              decode_token)
from db.redis import get_redis

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
        redis: Redis = Depends(get_redis)
) -> LoginUserResponseSchema:
    """User login endpoint by email and password."""
    response = await user_service.check_user(user_dto)
    if not response:
        raise AuthException(
            message="Incorrect email or password.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    tokens = await create_tokens(response.id, redis)
    return LoginUserResponseSchema(**tokens)


@router.get(
    path='/refresh/',
    response_model=LoginUserResponseSchema,
    summary='Обновления refresh token',
    description='Получение новых access token и refresh token',
    tags=['Обновление токена'],
)
async def refresh_token(
        refresh_info: RefreshTokenUserSchema = Depends(),
        redis: Redis = Depends(get_redis),
) -> LoginUserResponseSchema:
    """Get new access and refresh tokens."""
    if not await check_refresh_token(
            refresh_info.refresh_token,
            redis,
    ):
        raise AuthException(
            message="Incorrect token.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    response = await decode_token(refresh_info.refresh_token)
    _new_tokens = await create_tokens(response['user_id'], redis)
    await delete_refresh_token(refresh_info.refresh_token, redis)
    return LoginUserResponseSchema(**_new_tokens)


@router.get(
    path='/logout/',
    summary='Выход из профиля',
    description='Выход из профиля по access token',
    tags=['Logout', ],
)
async def logout_user(
        refresh_info: RefreshTokenUserSchema = Depends(),
        redis: Redis = Depends(get_redis),
) -> dict:
    """Logout endpoint by access token."""
    await delete_refresh_token(refresh_info.refresh_token, redis)
    return {'detail': 'logout is successfully'}
