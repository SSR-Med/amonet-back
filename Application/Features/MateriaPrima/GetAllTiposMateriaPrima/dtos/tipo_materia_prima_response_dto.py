from uuid import UUID


class TipoMateriaPrimaResponseDto:
    def __init__(self, id: UUID, nombre: str) -> None:
        self.id = id
        self.nombre = nombre
