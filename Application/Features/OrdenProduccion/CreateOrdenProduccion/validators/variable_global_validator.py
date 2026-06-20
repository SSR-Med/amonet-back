from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.CreateOrdenProduccion.dtos import (
    VariableGlobalDto,
)
from core.exceptions import NotFoundException
from infrastructure.dataaccess.configurations import (
    VariablesGlobalesMateriaPrimaConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class VariableGlobalValidator:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, VariablesGlobalesMateriaPrimaConfiguration)

    async def validate(self, variables_globales: List[VariableGlobalDto]) -> None:
        if not variables_globales:
            return

        for vg in variables_globales:
            existing = await self._repository.first_or_default(
                lambda q: q.where(
                    VariablesGlobalesMateriaPrimaConfiguration.id_amonet_variable_materia_prima
                    == vg.amonet_variable_materia_prima_id
                )
            )
            if existing is None:
                raise NotFoundException(
                    "VariableGlobalMateriaPrima",
                    str(vg.amonet_variable_materia_prima_id),
                )
