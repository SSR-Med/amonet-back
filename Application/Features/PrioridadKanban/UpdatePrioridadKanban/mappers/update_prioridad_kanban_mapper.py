from Application.Features.PrioridadKanban.UpdatePrioridadKanban.command import (
    UpdatePrioridadKanbanCommand,
)
from infrastructure.dataaccess.configurations import PrioridadKanbanConfiguration


class UpdatePrioridadKanbanMapper:

    @staticmethod
    def apply(
        model: PrioridadKanbanConfiguration,
        dto: UpdatePrioridadKanbanCommand,
    ) -> PrioridadKanbanConfiguration:
        model.nombre = dto.nombre
        model.color_red = dto.color_red
        model.color_green = dto.color_green
        model.color_blue = dto.color_blue
        return model
