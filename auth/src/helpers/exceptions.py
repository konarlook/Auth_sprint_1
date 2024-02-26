from abc import ABC, abstractproperty

from fastapi import status


class _BaseException(ABC, Exception):
    def __init__(self):
        self.message = ...
        self.status = ...


class AuthException(_BaseException):
    def __init__(self):
        self.message = "User already exist."
        self.status = status.HTTP_409_CONFLICT
