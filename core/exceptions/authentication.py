from .base import DomainException


class AuthenticationException(DomainException):
    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(message=message, code="AUTHENTICATION_ERROR")
