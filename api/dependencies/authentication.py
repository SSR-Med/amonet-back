from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dtos import CurrentUserDto
from core.exceptions import AuthenticationException
from infrastructure.dataaccess import get_async_session
from infrastructure.dataaccess.configurations import UsuarioConfiguration
from infrastructure.services import JwtService

security = HTTPBearer(scheme_name="BearerAuth")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session),
) -> CurrentUserDto:
    token = credentials.credentials

    try:
        payload = JwtService.decode(token)
    except Exception:
        raise AuthenticationException("Invalid or expired token")

    result = await session.execute(
        select(UsuarioConfiguration).where(
            UsuarioConfiguration.id_amonet_usuario == payload["sub"]
        )
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise AuthenticationException("User not found")

    if not user.activo:
        raise AuthenticationException("User is inactive")

    return CurrentUserDto(
        id=user.id_amonet_usuario,
        documento=user.documento,
        nombre=user.nombre,
        rol=user.rol,
    )
