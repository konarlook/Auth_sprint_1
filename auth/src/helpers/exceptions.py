from abc import ABC, abstractproperty

from fastapi import status


class AuthException(Exception):
    def __init__(self, message: str, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status = status_code
