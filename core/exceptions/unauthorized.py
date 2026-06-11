from .base import DomainException


class UnauthorizedException(DomainException):
    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(message=message, code="UNAUTHORIZED")
