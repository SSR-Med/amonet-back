from uuid import UUID

from core.exceptions import ConflictException
from infrastructure.dataaccess.configurations import ColumnaKanbanConfiguration
from infrastructure.dataaccess.repository import Repository


class UpdateColumnaKanbanValidator:

    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    async def validate(self, nombre: str, posicion: int, exclude_id: UUID) -> None:
        if posicion <= 0:
            raise ConflictException("Position must be greater than 0")

        existing_by_name = await self._repository.first_or_default(
            lambda q: q.where(
                ColumnaKanbanConfiguration.nombre == nombre,
                ColumnaKanbanConfiguration.id_amonet_columna_kanban != exclude_id,
            )
        )
        if existing_by_name is not None:
            raise ConflictException(f"Column name '{nombre}' already exists")

        existing_by_pos = await self._repository.first_or_default(
            lambda q: q.where(
                ColumnaKanbanConfiguration.posicion == posicion,
                ColumnaKanbanConfiguration.id_amonet_columna_kanban != exclude_id,
            )
        )
        if existing_by_pos is not None:
            raise ConflictException(f"Position {posicion} already in use")
