from Application.Features.TagKanban.UpdateTagKanban.command import (
    UpdateTagKanbanCommand,
)
from infrastructure.dataaccess.configurations import TagKanbanConfiguration


class UpdateTagKanbanMapper:

    @staticmethod
    def apply(
        model: TagKanbanConfiguration,
        dto: UpdateTagKanbanCommand,
    ) -> TagKanbanConfiguration:
        model.nombre = dto.nombre
        model.color_red = dto.color_red
        model.color_green = dto.color_green
        model.color_blue = dto.color_blue
        return model
