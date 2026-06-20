from datetime import datetime
from typing import List, Optional
from uuid import UUID


class UsuarioInfoDto:
    def __init__(self, id: UUID, documento: str, nombre: str) -> None:
        self.id = id
        self.documento = documento
        self.nombre = nombre


class ContenedorDto:
    def __init__(self, id: UUID, contador: int, cantidad: float, cantidad_disponible: float, precio: int, precio_unidad: float) -> None:
        self.id = id
        self.contador = contador
        self.cantidad = cantidad
        self.cantidad_disponible = cantidad_disponible
        self.precio = precio
        self.precio_unidad = precio_unidad


class InventarioResponseDto:
    def __init__(
        self,
        id: UUID,
        fecha_ingreso: datetime,
        numero_ingreso: str,
        amonet_materia_prima_id: UUID,
        materia_prima_nombre: str,
        unidad_abreviacion: str,
        proveedor: str,
        lote: str,
        fecha_vencimiento: datetime,
        usuario_alta: UsuarioInfoDto,
        status: Optional[bool],
        observacion_rechazo: Optional[str],
        fecha_modifica: Optional[datetime],
        usuario_modifica: Optional[UsuarioInfoDto],
        ruta_evidencia: str,
        cantidad_total: float,
        numero_contenedores: int,
        contenedores: List[ContenedorDto],
    ) -> None:
        self.id = id
        self.fecha_ingreso = fecha_ingreso
        self.numero_ingreso = numero_ingreso
        self.amonet_materia_prima_id = amonet_materia_prima_id
        self.materia_prima_nombre = materia_prima_nombre
        self.unidad_abreviacion = unidad_abreviacion
        self.proveedor = proveedor
        self.lote = lote
        self.fecha_vencimiento = fecha_vencimiento
        self.usuario_alta = usuario_alta
        self.status = status
        self.observacion_rechazo = observacion_rechazo
        self.fecha_modifica = fecha_modifica
        self.usuario_modifica = usuario_modifica
        self.ruta_evidencia = ruta_evidencia
        self.cantidad_total = cantidad_total
        self.numero_contenedores = numero_contenedores
        self.contenedores = contenedores
