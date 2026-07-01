from uuid import UUID


class TagKanbanResponseDto:
    def __init__(self, id: UUID, nombre: str, color_red: int, color_green: int, color_blue: int, activo: bool) -> None:
        self.id = id
        self.nombre = nombre
        self.color_red = color_red
        self.color_green = color_green
        self.color_blue = color_blue
        self.activo = activo
