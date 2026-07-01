from uuid import UUID

from core.exceptions import ConflictException
from infrastructure.dataaccess.configurations import TareaSprintConfiguration
from infrastructure.dataaccess.repository import Repository


class CreateComentarioTareaValidator:

    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    async def validate(self, amonet_tarea_sprint_id: UUID) -> None:
        tarea = await self._repository.first_or_default(
            lambda q: q.where(
                TareaSprintConfiguration.id_amonet_tarea_sprint == amonet_tarea_sprint_id
            )
        )
        if tarea is None:
            raise ConflictException("Tarea not found")
