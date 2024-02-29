from fastapi import APIRouter, Depends, status, Response, Cookie, Request
from fastapi.security import HTTPBasic
from redis.asyncio import Redis

from schemas import users
from schemas.histories import HistoryBase
from services.user_service import AuthUserService, get_user_service
from services.history_service import HistoryService, get_history_service
from helpers.exceptions import AuthException
from helpers import password
from db.redis import get_redis

router = APIRouter(prefix='/auth', tags=['Auth'])
security = HTTPBasic()


@router.post(
    path="/signup/",
    response_model=users.UserBaseSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Регистрация пользователя',
    description='Регистрация пользователя по обязательным полям',
    tags=['Страница регистрации'],
)
async def create_user(
        user_dto: users.CreateUserSchema = Depends(),
        user_service: AuthUserService = Depends(get_user_service)
) -> users.UserBaseSchema:
    """User registration endpoint by required fields."""
    request_email = await user_service.get(email=user_dto.email)
    if request_email:
        raise AuthException(
            message="User already exists",
            status_code=status.HTTP_409_CONFLICT,
        )
    user = await user_service.create(user_dto=user_dto)
    return user


@router.post(
    path="/login/",
    summary='Авторизация пользователя',
    description='Регистрация пользователя по логину и паролю',
    tags=['Основная страница', 'Авторизация пользователя'],
)
async def login_user(
        response: Response,
        request: Request,
        user_dto: users.LoginUserSchema = Depends(),
        user_service: AuthUserService = Depends(get_user_service),
        history_service: HistoryService = Depends(get_history_service),
        redis: Redis = Depends(get_redis),

) -> dict:
    """User login endpoint by email and password."""
    user_dto = await user_service.check_user(user_dto)
    if not user_dto:
        raise AuthException(
            message="Incorrect email or password.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    tokens = await password.create_tokens(user_dto.id, redis)
    response.set_cookie(
        'access_token', tokens['access_token'], httponly=True, max_age=20)
    response.set_cookie(
        'refresh_token', tokens['refresh_token'], httponly=True, max_age=40)
    session = await history_service.create(
        user_id=user_dto.id,
        device_id=request.headers.get('User-Agent'),
    )
    response.set_cookie(
        'session_id', session, httponly=True,
    )
    return {"detail": session}


@router.get(
    path='/refresh/',
    summary='Обновления refresh token',
    description='Получение новых access token и refresh token',
    tags=['Обновление токена'],
)
async def refresh_token(
        response: Response,
        refresh_token: str = Cookie(None),
        redis: Redis = Depends(get_redis),
) -> dict:
    """Get new access and refresh tokens."""
    if not await password.check_refresh_token(
            refresh_token,
            redis,
    ):
        raise AuthException(
            message="Incorrect token.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    user_info = await password.decode_token(refresh_token)
    _new_tokens = await password.create_tokens(user_info, redis)
    await password.delete_refresh_token(refresh_token, redis)
    response.set_cookie(
        'access_token', _new_tokens['access_token'], httponly=True, max_age=20)
    response.set_cookie(
        'refresh_token', _new_tokens['refresh_token'], httponly=True, max_age=40)
    return {"detail": "Successfully refresh"}


@router.post(
    path='/logout/',
    summary='Выход из профиля',
    description='Выход из профиля по access token',
    tags=['Logout', ],
)
async def logout_user(
        response: Response,
        refresh_token: str | None = Cookie(None),
        redis: Redis = Depends(get_redis),
) -> dict:
    """Logout endpoint by access token."""
    await password.delete_refresh_token(refresh_token, redis)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return {'detail': 'logout is successfully'}
