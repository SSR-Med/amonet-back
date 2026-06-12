from uuid import UUID


class CurrentUsuarioResponseDto:
    def __init__(self, id: UUID, documento: str, nombre: str, rol: str) -> None:
        self.id = id
        self.documento = documento
        self.nombre = nombre
        self.rol = rol
