from typing import List, Optional
from uuid import UUID

from core.exceptions import ConflictException
from infrastructure.dataaccess.configurations import (
    ColumnaKanbanConfiguration,
    SprintConfiguration,
    PrioridadKanbanConfiguration,
    TagKanbanConfiguration,
    UsuarioConfiguration,
)
from infrastructure.dataaccess.repository import Repository


class CreateTareaSprintValidator:

    def __init__(
        self,
        sprint_repository: Repository,
        columna_repository: Repository,
        usuario_repository: Repository,
        prioridad_repository: Repository,
        tag_repository: Repository,
    ) -> None:
        self._sprint_repository = sprint_repository
        self._columna_repository = columna_repository
        self._usuario_repository = usuario_repository
        self._prioridad_repository = prioridad_repository
        self._tag_repository = tag_repository

    async def validate(
        self,
        amonet_sprint_id: UUID,
        amonet_columna_kanban_id: UUID,
        asignado: UUID,
        amonet_prioridad_kanban_id: Optional[UUID] = None,
        tags: Optional[List[UUID]] = None,
    ) -> None:
        sprint = await self._sprint_repository.first_or_default(
            lambda q: q.where(SprintConfiguration.id_amonet_sprint == amonet_sprint_id)
        )
        if sprint is None:
            raise ConflictException("Sprint not found")

        columna = await self._columna_repository.first_or_default(
            lambda q: q.where(
                ColumnaKanbanConfiguration.id_amonet_columna_kanban == amonet_columna_kanban_id
            )
        )
        if columna is None:
            raise ConflictException("Column not found")

        usuario = await self._usuario_repository.first_or_default(
            lambda q: q.where(UsuarioConfiguration.id_amonet_usuario == asignado)
        )
        if usuario is None:
            raise ConflictException("Assigned user not found")

        if amonet_prioridad_kanban_id:
            prioridad = await self._prioridad_repository.first_or_default(
                lambda q: q.where(PrioridadKanbanConfiguration.id_amonet_prioridad_kanban == amonet_prioridad_kanban_id)
            )
            if prioridad is None:
                raise ConflictException("Priority not found")

        if tags:
            for tag_id in tags:
                tag = await self._tag_repository.first_or_default(
                    lambda q: q.where(TagKanbanConfiguration.id_amonet_tag_kanban == tag_id)
                )
                if tag is None:
                    raise ConflictException(f"TagKanban '{tag_id}' not found")
