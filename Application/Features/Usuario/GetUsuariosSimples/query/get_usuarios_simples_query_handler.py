from typing import List, Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class UsuarioSimpleDto:
    def __init__(self, id: UUID, documento: str, nombre: str) -> None:
        self.id = id
        self.documento = documento
        self.nombre = nombre


class GetUsuariosSimplesQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def handle(
        self,
        documento: Optional[str] = None,
        nombre: Optional[str] = None,
    ) -> List[UsuarioSimpleDto]:
        from infrastructure.dataaccess.configurations import UsuarioConfiguration

        query = select(
            UsuarioConfiguration.id_amonet_usuario,
            UsuarioConfiguration.documento,
            UsuarioConfiguration.nombre,
        ).where(UsuarioConfiguration.activo == True)

        if documento:
            query = query.where(
                func.upper(UsuarioConfiguration.documento).like(
                    f"%{documento.strip().upper()}%"
                )
            )
        if nombre:
            query = query.where(
                func.upper(UsuarioConfiguration.nombre).like(
                    f"%{nombre.strip().upper()}%"
                )
            )

        query = query.order_by(UsuarioConfiguration.documento.asc())

        result = await self._session.execute(query)
        return [
            UsuarioSimpleDto(id=row[0], documento=row[1], nombre=row[2])
            for row in result.all()
        ]
