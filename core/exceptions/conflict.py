from .base import DomainException


class ConflictException(DomainException):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="CONFLICT")
