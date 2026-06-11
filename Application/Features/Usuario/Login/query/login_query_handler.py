from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Usuario.Login.dtos import LoginResponseDto
from Application.Features.Usuario.Login.query import LoginQuery
from core.dtos import JwtUserDto
from core.exceptions import UnauthorizedException
from infrastructure.dataaccess.configurations import UsuarioConfiguration
from infrastructure.services import JwtService, PasswordService


class LoginQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def handle(self, query: LoginQuery) -> LoginResponseDto:
        result = await self._session.execute(
            select(UsuarioConfiguration).where(
                func.upper(func.trim(UsuarioConfiguration.documento))
                == query.documento.strip().upper()
            )
        )
        user = result.scalar_one_or_none()

        if user is None or not PasswordService.verify(query.password, user.password):
            raise UnauthorizedException("Invalid credentials")

        jwt_user = JwtUserDto(
            user_id=user.id_amonet_usuario,
            documento=user.documento,
            nombre=user.nombre,
            rol=user.rol,
        )
        token = JwtService.generate(jwt_user)

        return LoginResponseDto(
            token=token,
            id=user.id_amonet_usuario,
            documento=user.documento,
            nombre=user.nombre,
            rol=user.rol,
        )
