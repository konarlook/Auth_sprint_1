from fastapi import APIRouter, Depends, status, Response, Cookie, Request, HTTPException
from fastapi.responses import RedirectResponse
from redis.asyncio import Redis

from core.config import settings
from core.constants import UserRoleEnum
from db.redis import get_redis
from helpers import access
from schemas import histories
from schemas import users, roles, jwt_schemas
from schemas.base import Page
from services.auth_service import AuthJWT, get_auth_jwt
from services.history_service import HistoryService, get_history_service
from services.role_service import AuthRoleService, get_role_service
from services.user_service import AuthUserService, get_user_service
from services.oauth_service import OAuthService, get_oauth_service

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
    if not "".join(user_dto.hashed_password.split()):
        raise HTTPException(
            detail="Password must be set.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    request_email = await user_service.get(email=user_dto.email)
    if request_email:
        raise HTTPException(
            detail="User already exists",
            status_code=status.HTTP_409_CONFLICT,
        )
    if user_dto.user_name:
        request_username = await user_service.get_by_username(
            username=user_dto.user_name
        )
        if request_username:
            raise HTTPException(
                detail="Username already exists.",
                status_code=status.HTTP_409_CONFLICT,
            )

    user_encode = await user_service.create(user_dto=user_dto)
    user = users.UserBaseSchema(email=user_encode["email"])
    await role_service.set_role(
        user_role=roles.UserRoleDto(
            user_email=user_encode["email"], role_name=UserRoleEnum.DefaultUser.value
        )
    )
    return user


@router.post(
    path="/login/",
    status_code=status.HTTP_200_OK,
    summary="Авторизация пользователя",
    description="Регистрация пользователя по логину и паролю",
)
async def login_user(
        response: Response,
        request: Request,
        user_dto: users.LoginUserSchema = Depends(),
        user_service: AuthUserService = Depends(get_user_service),
        history_service: HistoryService = Depends(get_history_service),
        auth_service: AuthJWT = Depends(get_auth_jwt),
        redis: Redis = Depends(get_redis),
) -> dict:
    """User login endpoint by email and password."""
    user_dto = await user_service.check_user(user_dto)
    if not user_dto:
        raise HTTPException(
            detail="Incorrect email or password.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    user_agent = await history_service.create(
        user_id=user_dto.id,
        device_id=request.headers.get("User-Agent"),
    )

    action = await user_service.get_role(user_dto)

    tokens = await auth_service.create_tokens(
        data=user_dto,
        user_agent=user_agent,
        actions=action,
        redis=redis,
    )
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        max_age=settings.auth_jwt.access_token_lifetime,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=settings.auth_jwt.refresh_token_lifetime,
    )
    return {"detail": "login successful"}


@router.post(
    path="/login/{provider}/",
    status_code=status.HTTP_200_OK,
    summary="Аунтификация через соц. сети",
    description="Аунтификация по протоколу OAuth2 через социальные сети",
)
async def login_oauth(
        request: Request,
        provider: str,
        oauth_service: OAuthService = Depends(get_oauth_service),
) -> RedirectResponse:
    return await oauth_service.redirect(request, provider)


@router.get(
    path="/login/{provider}/callback",
    status_code=status.HTTP_200_OK,
    # response_model=jwt_schemas.ResponseTokenSchema,
)
async def login_oauth_callback(
        code: str,
        state: str,
        request: Request,
        provider: str,
        user_service: AuthUserService = Depends(get_user_service),
        history_service: HistoryService = Depends(get_history_service),
        auth_service: AuthJWT = Depends(get_auth_jwt),
        redis: Redis = Depends(get_redis),
        oauth_service: OAuthService = Depends(get_oauth_service),
) -> jwt_schemas.ResponseTokenSchema:
    if state != request.session.get("state"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="State is incorrect",
        )
    request_url = request.url_for("login_oauth_callback", provider=provider)
    user = None
    if provider == "yandex":
        user = await oauth_service.get_user(code, request_url)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    redirect = RedirectResponse(url="/")
    user_agent = await history_service.create(
        user_id=user.id,
        device_id=request.headers.get("User-Agent"),
    )

    action = await user_service.get_role(user)

    tokens = await auth_service.create_tokens(
        data=user,
        user_agent=user_agent,
        actions=action,
        redis=redis,
    )
    redirect.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        max_age=settings.auth_jwt.access_token_lifetime,
    )
    redirect.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=settings.auth_jwt.refresh_token_lifetime,
    )
    return {"detail": "login successful"}


@router.put(
    path="/change_password/",
    status_code=status.HTTP_200_OK,
    summary="Изменение пароля",
    description="Изменить пароль по access token",
)
@access.check_access_token
async def change_password(
        access_token: str | None = Cookie(None),
        user_service: AuthUserService = Depends(get_user_service),
        auth_service: AuthJWT = Depends(get_auth_jwt),
        password_data: users.ChangePasswordSchema = Depends(),
) -> dict:
    """Change password by access token."""
    user_info = await auth_service.decode_jwt(access_token)
    await user_service.update(user_info["sub"], password_data)
    return {"detail": "Successfully changed password."}


@router.get(
    path="/refresh/",
    summary="Обновления refresh token",
    description="Получение новых access token и refresh token",
)
async def refresh(
        response: Response,
        refresh_token: str = Cookie(None),
        user_service: AuthUserService = Depends(get_user_service),
        auth_service: AuthJWT = Depends(get_auth_jwt),
        redis: Redis = Depends(get_redis),
) -> dict:
    """Get new access and refresh tokens."""
    if not await auth_service.check_refresh_token(
            refresh_token,
            redis,
    ):
        raise HTTPException(
            detail="Incorrect token.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    user_info = await auth_service.decode_jwt(refresh_token)
    user_info = jwt_schemas.RefreshJWTSchema(**user_info)
    action = await user_service.get_role(user_info)

    user_agent = user_info.client_id

    _new_tokens = await auth_service.create_tokens(
        data=user_info,
        user_agent=user_agent,
        actions=action,
        redis=redis,
    )
    await auth_service.delete_refresh_token(refresh_token, redis)
    response.set_cookie(
        key="access_token",
        value=_new_tokens.access_token,
        httponly=True,
        max_age=settings.auth_jwt.access_token_lifetime,
    )
    response.set_cookie(
        key="refresh_token",
        value=_new_tokens.refresh_token,
        httponly=True,
        max_age=settings.auth_jwt.refresh_token_lifetime,
    )
    return {"detail": "Successfully refresh"}


@router.post(
    path="/logout/",
    summary="Выход из профиля",
    description="Выход из профиля по refresh token",
)
async def logout(
        response: Response,
        refresh_token: str | None = Cookie(None),
        auth_service: AuthJWT = Depends(get_auth_jwt),
        history_service: HistoryService = Depends(get_history_service),
        redis: Redis = Depends(get_redis),
) -> dict:
    """Logout endpoint by access token."""
    user_info = await auth_service.decode_jwt(refresh_token)
    delite = await auth_service.delete_refresh_token(refresh_token, redis)
    if not delite:
        raise HTTPException(
            detail="Incorrect command.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    await history_service.update(user_info["client_id"])
    return {"detail": "logout is successfully"}


@router.get(
    path="/history/",
    response_model=Page[histories.FullHistorySchema],
    summary="Получение пользовательской истории",
    description="Получение истории пользователя по access token",
)
@access.check_access_token
async def history(
        access_token: str = Cookie(None),
        auth_service: AuthJWT = Depends(get_auth_jwt),
        history_service: HistoryService = Depends(get_history_service),
        history_data: histories.HistoryRequestSchema = Depends(),
) -> list[histories.FullHistorySchema]:
    """Get user history by access token."""
    user_info = await auth_service.decode_jwt(access_token)
    list_history = await history_service.get(user_info["sub"], history_data)
    return list_history
