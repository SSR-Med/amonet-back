from uuid import UUID


class VariablesGlobalesMateriaPrimaResponseDto:
    def __init__(self, id: UUID, nombre: str) -> None:
        self.id = id
        self.nombre = nombre
