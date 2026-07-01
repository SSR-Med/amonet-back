from Application.Features.PrioridadKanban.CreatePrioridadKanban.dtos import (
    PrioridadKanbanResponseDto,
)
from infrastructure.dataaccess.configurations import PrioridadKanbanConfiguration


class PrioridadKanbanMapper:

    @staticmethod
    def to_response(model: PrioridadKanbanConfiguration) -> PrioridadKanbanResponseDto:
        return PrioridadKanbanResponseDto(
            id=model.id_amonet_prioridad_kanban,
            nombre=model.nombre,
            color_red=model.color_red,
            color_green=model.color_green,
            color_blue=model.color_blue,
            activo=model.activo,
        )
