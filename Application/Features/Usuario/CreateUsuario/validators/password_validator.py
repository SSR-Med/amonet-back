from core.constants import MIN_PASSWORD_LENGTH
from core.exceptions import BadRequestException

COMMON_PASSWORDS = {
    "123456789012",
    "password1234",
    "contrasena123",
    "qwertyuiop12",
    "administrador",
    "amonet123456",
}


class PasswordValidator:
    @staticmethod
    def validate(password: str) -> None:
        if len(password) < MIN_PASSWORD_LENGTH:
            raise BadRequestException(
                f"La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres"
            )

        if password.lower() in COMMON_PASSWORDS:
            raise BadRequestException("La contraseña es demasiado común")
