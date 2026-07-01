from uuid import uuid4

from Application.Features.PrioridadKanban.CreatePrioridadKanban.command import (
    CreatePrioridadKanbanCommand,
)
from infrastructure.dataaccess.configurations import PrioridadKanbanConfiguration


class CreatePrioridadKanbanMapper:

    @staticmethod
    def to_model(dto: CreatePrioridadKanbanCommand) -> PrioridadKanbanConfiguration:
        return PrioridadKanbanConfiguration(
            id_amonet_prioridad_kanban=uuid4(),
            nombre=dto.nombre,
            color_red=dto.color_red,
            color_green=dto.color_green,
            color_blue=dto.color_blue,
        )
