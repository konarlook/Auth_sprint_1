from abc import ABC, abstractmethod

from functools import lru_cache
from authlib.integrations.starlette_client import OAuth, OAuthError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from repositories.user_data_repository import get_database_client, UserDataRepository
from models.oauth import SocialNetworks
from models.auth_orm_models import UserDataOrm
from schemas.jwt_schemas import ResponseTokenSchema
from .auth_service import AuthJWT, get_auth_jwt
from .user_service import AuthUserService, get_user_service
from helpers.random import get_random_string


class OAuthBaseProvider(ABC):
    def __init__(self, client, provider):
        self.client = client
        self.provider = provider

    @abstractmethod
    async def received_token(self, token):
        raise NotImplementedError

    async def redirect(self, request) -> RedirectResponse:
        redirect_uri = request.url_for('auth_callback', provider=self.provider)
        return await self.client.authorize_redirect(redirect_uri)

    async def check_access_token(self, request):
        return await self.client.authorize_access_token(request)


class YandexOAuthProvider(OAuthBaseProvider):
    def __init__(self, client):
        super().__init__(client, "yandex")

    async def received_token(self, token):
        pass


class OAuthFactory:
    @staticmethod
    def create_oauth_provider(name: str, client):
        if name == 'yandex':
            return YandexOAuthProvider(client=client)


class OAuthService:
    async def redirect(self, request: Request, provider: str) -> RedirectResponse:
        redirect_uri = request.url_for("login_oauth_callback", provider=provider)
        state = get_random_string(16)
        request.session["state"] = state

        if provider == "yandex":
            return RedirectResponse(
                f"https://oauth.yandex.ru/authorize"
                f"?response_type=code"
                f"&client_id=c55ab5b5328248ef86f61d33354f6f4b"
                f"&redirect_uri={redirect_uri}"
                f"&state={state}"
            )

@lru_cache
def get_oauth_service(

) -> OAuthService:
    return OAuthService(

    )
