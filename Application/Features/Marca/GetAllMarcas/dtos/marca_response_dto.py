from uuid import UUID


class MarcaResponseDto:
    def __init__(self, id: UUID, nombre: str) -> None:
        self.id = id
        self.nombre = nombre
