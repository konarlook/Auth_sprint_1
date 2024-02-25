from abc import ABC, abstractproperty

from fastapi import status


class _BaseException(ABC, Exception):
    @abstractproperty
    def message(self):
        """Message displayed to the user."""
        raise NotImplementedError

    @abstractproperty
    def status(self):
        """Status displayed to the user."""
        raise NotImplementedError


class AuthException(_BaseException):
    def __init__(self):
        self.message = "User already exist."
        self.status = status.HTTP_409_CONFLICT

    @message.setter
    def message(self, value):
        self._message = value

    @status.setter
    def status(self, value):
        self._status = value
