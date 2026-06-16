from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.MateriaPrima.GetVariableGlobalById.query import (
    GetVariableGlobalByIdQuery,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.dtos import (
    VariablesGlobalesMateriaPrimaResponseDto,
)
from Application.Features.MateriaPrima.GetAllVariablesGlobales.mappers import (
    VariablesGlobalesMateriaPrimaMapper,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class GetVariableGlobalByIdQueryHandler:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, VariablesGlobalesMateriaPrimaConfiguration)

    async def handle(
        self, query: GetVariableGlobalByIdQuery
    ) -> VariablesGlobalesMateriaPrimaResponseDto:
        model = await self._repository.first_or_default(
            lambda q: q.where(
                VariablesGlobalesMateriaPrimaConfiguration.id_amonet_variable_materia_prima == query.id
            )
        )
        if model is None:
            raise NotFoundException("VariableGlobal", str(query.id))
        return VariablesGlobalesMateriaPrimaMapper.to_response(model)
