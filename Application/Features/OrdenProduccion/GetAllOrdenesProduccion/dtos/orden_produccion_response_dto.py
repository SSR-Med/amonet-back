from datetime import datetime
from typing import List, Optional
from uuid import UUID


class ProductoInfoDto:
    def __init__(self, id: UUID, codigo: str, nombre: str, marca_nombre: str) -> None:
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.marca_nombre = marca_nombre


class UsuarioInfoDto:
    def __init__(self, id: UUID, documento: str, nombre: str) -> None:
        self.id = id
        self.documento = documento
        self.nombre = nombre


class EstadoProduccionInfoDto:
    def __init__(self, id: UUID, nombre: str) -> None:
        self.id = id
        self.nombre = nombre


class VariableGlobalResponseDto:
    def __init__(self, id: UUID, nombre: str, cantidad: int) -> None:
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad


class ContenedorResponseDto:
    def __init__(
        self,
        id: UUID,
        cantidad: int,
        coste: float,
        lote: str,
        proveedor: str,
    ) -> None:
        self.id = id
        self.cantidad = cantidad
        self.coste = coste
        self.lote = lote
        self.proveedor = proveedor


class MateriaPrimaResponseDto:
    def __init__(
        self,
        id: UUID,
        nombre: str,
        contenedores: List[ContenedorResponseDto],
    ) -> None:
        self.id = id
        self.nombre = nombre
        self.contenedores = contenedores


class OrdenProduccionResponseDto:
    def __init__(
        self,
        id: UUID,
        descripcion: str,
        observacion_creacion: Optional[str],
        fecha_alta: datetime,
        fecha_modifica: Optional[datetime],
        coste: float,
        producto: ProductoInfoDto,
        estado_produccion: EstadoProduccionInfoDto,
        usuario_alta: UsuarioInfoDto,
        usuario_modifica: Optional[UsuarioInfoDto],
        variables_globales: List[VariableGlobalResponseDto],
        materias_primas: List[MateriaPrimaResponseDto],
    ) -> None:
        self.id = id
        self.descripcion = descripcion
        self.observacion_creacion = observacion_creacion
        self.fecha_alta = fecha_alta
        self.fecha_modifica = fecha_modifica
        self.coste = coste
        self.producto = producto
        self.estado_produccion = estado_produccion
        self.usuario_alta = usuario_alta
        self.usuario_modifica = usuario_modifica
        self.variables_globales = variables_globales
        self.materias_primas = materias_primas
