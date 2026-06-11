from datetime import datetime, timedelta, timezone

import jwt

from core.dtos import JwtUserDto
from infrastructure.services.settings_service import get_settings


class JwtService:

    @staticmethod
    def generate(user: JwtUserDto) -> str:
        settings = get_settings()
        payload = {
            "sub": str(user.user_id),
            "documento": user.documento,
            "nombre": user.nombre,
            "rol": user.rol,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
