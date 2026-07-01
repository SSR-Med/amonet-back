from uuid import uuid4

from Application.Features.TagKanban.CreateTagKanban.command import (
    CreateTagKanbanCommand,
)
from infrastructure.dataaccess.configurations import TagKanbanConfiguration


class CreateTagKanbanMapper:

    @staticmethod
    def to_model(dto: CreateTagKanbanCommand) -> TagKanbanConfiguration:
        return TagKanbanConfiguration(
            id_amonet_tag_kanban=uuid4(),
            nombre=dto.nombre,
            color_red=dto.color_red,
            color_green=dto.color_green,
            color_blue=dto.color_blue,
        )
