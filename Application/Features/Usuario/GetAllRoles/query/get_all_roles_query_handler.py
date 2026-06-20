from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.Usuario.GetAllRoles.dtos import RolResponseDto
from Application.Features.Usuario.GetAllRoles.mappers import RolMapper
from Application.Features.Usuario.GetAllRoles.query import GetAllRolesQuery
from infrastructure.dataaccess.configurations import (
    CatalogoUsuarioRolConfiguration,
)


class GetAllRolesQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def handle(self, query: GetAllRolesQuery) -> List[RolResponseDto]:
        result = await self._session.execute(
            select(CatalogoUsuarioRolConfiguration)
            .where(CatalogoUsuarioRolConfiguration.status == True)
            .order_by(CatalogoUsuarioRolConfiguration.nombre)
        )
        roles = result.scalars().all()
        return RolMapper.to_list_response(roles)
