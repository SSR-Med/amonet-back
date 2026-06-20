from sqlalchemy.ext.asyncio import AsyncSession

from Application.Features.OrdenProduccion.CreateOrdenProduccion.command import (
    CreateOrdenProduccionCommand,
)
from .contenedor_validator import ContenedorValidator
from .materia_prima_validator import MateriaPrimaValidator
from .product_validator import ProductValidator
from .variable_global_validator import VariableGlobalValidator


class CreateOrdenProduccionValidator:

    def __init__(self, session: AsyncSession) -> None:
        self._product_validator = ProductValidator(session)
        self._variable_global_validator = VariableGlobalValidator(session)
        self._materia_prima_validator = MateriaPrimaValidator(session)
        self._contenedor_validator = ContenedorValidator(session)

    async def validate(self, command: CreateOrdenProduccionCommand) -> None:
        await self._product_validator.validate(command.amonet_producto_id)
        await self._variable_global_validator.validate(command.variables_globales)
        await self._materia_prima_validator.validate(
            command.variables_globales, command.materias_primas, command.observaciones
        )
        await self._contenedor_validator.validate(command.materias_primas)
