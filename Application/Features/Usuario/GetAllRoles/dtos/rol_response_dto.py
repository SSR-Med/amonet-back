from uuid import UUID


class RolResponseDto:
    def __init__(self, id: UUID, nombre: str) -> None:
        self.id = id
        self.nombre = nombre
