from .base import DomainException


class BadRequestException(DomainException):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="BAD_REQUEST")
