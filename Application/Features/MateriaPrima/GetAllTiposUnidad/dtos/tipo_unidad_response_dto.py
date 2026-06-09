from uuid import UUID


class TipoUnidadResponseDto:
    def __init__(self, id: UUID, nombre: str, abreviacion: str) -> None:
        self.id = id
        self.nombre = nombre
        self.abreviacion = abreviacion
