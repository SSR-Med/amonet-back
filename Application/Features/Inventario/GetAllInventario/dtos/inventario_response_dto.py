from datetime import datetime
from typing import List, Optional
from uuid import UUID


class UsuarioInfoDto:
    def __init__(self, id: UUID, documento: str, nombre: str) -> None:
        self.id = id
        self.documento = documento
        self.nombre = nombre


class ContenedorDto:
    def __init__(self, contador: int, cantidad: float, precio: int, precio_unidad: float) -> None:
        self.contador = contador
        self.cantidad = cantidad
        self.precio = precio
        self.precio_unidad = precio_unidad


class InventarioResponseDto:
    def __init__(
        self,
        id: UUID,
        fecha_ingreso: datetime,
        numero_ingreso: str,
        materia_prima_nombre: str,
        unidad_abreviacion: str,
        proveedor: str,
        lote: str,
        fecha_vencimiento: datetime,
        usuario_alta: UsuarioInfoDto,
        status: Optional[bool],
        ruta_evidencia: str,
        cantidad_total: float,
        numero_contenedores: int,
        contenedores: List[ContenedorDto],
    ) -> None:
        self.id = id
        self.fecha_ingreso = fecha_ingreso
        self.numero_ingreso = numero_ingreso
        self.materia_prima_nombre = materia_prima_nombre
        self.unidad_abreviacion = unidad_abreviacion
        self.proveedor = proveedor
        self.lote = lote
        self.fecha_vencimiento = fecha_vencimiento
        self.usuario_alta = usuario_alta
        self.status = status
        self.ruta_evidencia = ruta_evidencia
        self.cantidad_total = cantidad_total
        self.numero_contenedores = numero_contenedores
        self.contenedores = contenedores
