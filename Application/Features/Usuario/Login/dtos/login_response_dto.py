from uuid import UUID


class LoginResponseDto:
    def __init__(self, token: str, id: UUID, documento: str, nombre: str, rol: str) -> None:
        self.token = token
        self.id = id
        self.documento = documento
        self.nombre = nombre
        self.rol = rol
