from abc import ABC, abstractmethod

from fastapi import Request


class OAuthBaseProvider(ABC):
    def __init__(self, client, provider):
        self.client = client
        self.provider = provider

    @abstractmethod
    async def received_token(self, token):
        raise NotImplementedError

    async def redirect(self, request: str):
        redirect_uri = request

    async def check_access_token(self, request):
        raise NotImplementedError


class YandexOAuthProvider(OAuthBaseProvider):
    pass


class GoogleOAuthProvider(OAuthBaseProvider):
    pass


class VkOAuthProvider(OAuthBaseProvider):
    pass
