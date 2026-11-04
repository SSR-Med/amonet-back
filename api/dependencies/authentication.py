from typing import Optional

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import AUTH_COOKIE
from core.dtos import CurrentUserDto
from core.exceptions import AuthenticationException
from infrastructure.dataaccess import get_async_session
from infrastructure.dataaccess.configurations import UsuarioConfiguration
from infrastructure.services import JwtService

security = HTTPBearer(scheme_name="BearerAuth", auto_error=False)


def _extract_token(
    request: Request, credentials: Optional[HTTPAuthorizationCredentials]
) -> str:
    if credentials is not None:
        return credentials.credentials

    token = request.cookies.get(AUTH_COOKIE)
    if not token:
        raise AuthenticationException("Missing credentials")

    return token


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: AsyncSession = Depends(get_async_session),
) -> CurrentUserDto:
    token = _extract_token(request, credentials)

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

    if payload.get("ver", 0) != user.token_version:
        raise AuthenticationException("Token revoked")

    return CurrentUserDto(
        id=user.id_amonet_usuario,
        documento=user.documento,
        nombre=user.nombre,
        rol=user.rol,
    )
