from Application.Features.TagKanban.CreateTagKanban.dtos import (
    TagKanbanResponseDto,
)
from infrastructure.dataaccess.configurations import TagKanbanConfiguration


class TagKanbanMapper:

    @staticmethod
    def to_response(model: TagKanbanConfiguration) -> TagKanbanResponseDto:
        return TagKanbanResponseDto(
            id=model.id_amonet_tag_kanban,
            nombre=model.nombre,
            color_red=model.color_red,
            color_green=model.color_green,
            color_blue=model.color_blue,
            activo=model.activo,
        )
