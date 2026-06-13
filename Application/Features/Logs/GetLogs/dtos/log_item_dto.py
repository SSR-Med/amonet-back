from typing import Optional


class LogItemDto:
    def __init__(self, nombre: str, peso: Optional[int], fecha: str, origen: str) -> None:
        self.nombre = nombre
        self.peso = peso
        self.fecha = fecha
        self.origen = origen
