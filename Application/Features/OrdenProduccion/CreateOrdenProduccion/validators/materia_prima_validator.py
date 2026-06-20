from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.CreateOrdenProduccion.dtos import (
    MateriaPrimaDto,
    VariableGlobalDto,
)
from core.exceptions import BadRequestException, NotFoundException
from infrastructure.dataaccess.configurations import MateriaPrimaConfiguration
from infrastructure.dataaccess.repository import Repository


class MateriaPrimaValidator:

    def __init__(self, session: AsyncSession) -> None:
        self._repository = Repository(session, MateriaPrimaConfiguration)

    async def validate(
        self,
        variables_globales: List[VariableGlobalDto],
        materias_primas: List[MateriaPrimaDto],
        observaciones: Optional[str] = None,
    ) -> None:
        for mp in materias_primas:
            if mp.cantidad <= 0:
                raise BadRequestException(
                    f"Materia prima '{mp.amonet_materia_prima_id}' must have a positive quantity"
                )

            for cont in mp.contenedores:
                if cont.cantidad <= 0:
                    raise BadRequestException(
                        f"Container '{cont.amonet_inventario_materia_prima_contenedor_id}' "
                        f"must have a positive quantity"
                    )
            existing = await self._repository.first_or_default(
                lambda q: q.where(
                    MateriaPrimaConfiguration.id_amonet_materia_prima
                    == mp.amonet_materia_prima_id
                )
            )
            if existing is None:
                raise NotFoundException("MateriaPrima", str(mp.amonet_materia_prima_id))

        if not variables_globales and (not observaciones or not observaciones.strip()):
            raise BadRequestException(
                "Observations are required when no global variables are provided"
            )
