from fastapi import APIRouter, Depends, status, Response, Cookie, Request, HTTPException
from redis.asyncio import Redis

from schemas import users, roles, histories
from services.role_service import AuthRoleService, get_role_service
from services.user_service import AuthUserService, get_user_service
from services.history_service import HistoryService, get_history_service
from helpers import password, access
from db.redis import get_redis
from core.constants import UserRoleEnum

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    path="/signup/",
    response_model=users.UserBaseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация пользователя",
    description="Регистрация пользователя по обязательным полям",
)
async def create_user(
        user_dto: users.CreateUserSchema = Depends(),
        user_service: AuthUserService = Depends(get_user_service),
        role_service: AuthRoleService = Depends(get_role_service),
) -> users.UserBaseSchema:
    """User registration endpoint by required fields."""
    request_email = await user_service.get(email=user_dto.email)
    if request_email:
        raise HTTPException(
            detail="User already exists",
            status_code=status.HTTP_409_CONFLICT,
        )
    user_encode = await user_service.create(user_dto=user_dto)
    user = users.UserBaseSchema(email=user_encode["email"])
    await role_service.set_role(
        user_role=roles.UserRoleDto(
            user_id=user_encode["id"], role_name=UserRoleEnum.DefaultUser.value
        )
    )
    return user


@router.post(
    path="/login/",
    summary="Авторизация пользователя",
    description="Регистрация пользователя по логину и паролю",
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
        raise HTTPException(
            detail="Incorrect email or password.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    client_id = await history_service.create(
        user_id=user_dto.id,
        device_id=request.headers.get("User-Agent"),
    )

    action = await user_service.get_role(user_dto)

    tokens = await password.create_tokens(
        user_dto.dict(),
        client_id=client_id,
        actions=action,
        redis=redis,
    )
    response.set_cookie(
        "access_token", tokens["access_token"], httponly=True, max_age=20
    )
    response.set_cookie(
        "refresh_token", tokens["refresh_token"], httponly=True, max_age=40
    )
    return {"detail": "login successful"}


@router.put(
    path='/change-password/',
    status_code=status.HTTP_200_OK,
    summary='Изменение пароля',
    description='Изменить пароль по access token',
)
@access.check_access_token
async def change_password(
        access_token: str | None = Cookie(None),
        user_service: AuthUserService = Depends(get_user_service),
        password_data: users.ChangePasswordSchema = Depends(),
) -> dict:
    """Change password by access token."""
    user_info = await password.decode_token(access_token)
    await user_service.update(user_info['sub'], password_data)
    return {"detail": "Successfully changed password."}


@router.get(
    path="/refresh/",
    summary="Обновления refresh token",
    description="Получение новых access token и refresh token",
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
        raise HTTPException(
            detail="Incorrect token.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    user_info = await password.decode_token(refresh_token)
    user_role = 'default'
    client_id = user_info["client_id"]
    _new_tokens = await password.create_tokens(
        user_info,
        client_id=client_id,
        role=user_role,
        redis=redis
    )
    await password.delete_refresh_token(refresh_token, redis)
    response.set_cookie(
        "access_token", _new_tokens["access_token"], httponly=True, max_age=20
    )
    response.set_cookie(
        "refresh_token", _new_tokens["refresh_token"], httponly=True, max_age=40
    )
    return {"detail": "Successfully refresh"}


@router.post(
    path="/logout/",
    summary="Выход из профиля",
    description="Выход из профиля по refresh token",
)
async def logout_user(
        response: Response,
        access_token: str | None = Cookie(None),
        refresh_token: str | None = Cookie(None),
        history_service: HistoryService = Depends(get_history_service),
        redis: Redis = Depends(get_redis),
) -> dict:
    """Logout endpoint by access token."""
    user_info = await password.decode_token(refresh_token)
    delite = await password.delete_refresh_token(refresh_token, redis)
    if not delite:
        raise HTTPException(
            detail='Incorrect command.',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    await history_service.update(user_info['client_id'])
    return {"detail": "logout is successfully"}


@router.get(
    path='/history/',
    response_model=list[histories.FullHistorySchema],
    summary='Получение пользовательской истории',
    description='Получение истории пользователя по access token',
)
@access.check_access_token
async def get_history(
        access_token: str = Cookie(None),
        history_service: HistoryService = Depends(get_history_service),
) -> list[histories.FullHistorySchema]:
    """Get user history by access token."""
    user_info = await password.decode_token(access_token)
    list_history = await history_service.get(user_info['sub'])
    return list_history
