import json
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import Request, UploadFile
from pydantic import BaseModel


class UpdateContenedorDto(BaseModel):
    contador: int
    cantidad: float
    cantidad_disponible: float
    precio: int


class UpdateInventarioCommand(BaseModel):
    fecha_ingreso: Optional[datetime] = None
    numero_ingreso: Optional[str] = None
    amonet_materia_prima_id: Optional[UUID] = None
    proveedor: Optional[str] = None
    lote: Optional[str] = None
    fecha_vencimiento: Optional[datetime] = None
    status: Optional[bool] = None
    observacion_rechazo: Optional[str] = None
    contenedores: Optional[List[UpdateContenedorDto]] = None
    archivo: Optional[bytes] = None
    nombre_archivo: Optional[str] = None

    @staticmethod
    async def from_request(request: Request, archivo: UploadFile, data: str) -> "UpdateInventarioCommand":
        if archivo is not None:
            parsed = json.loads(data) if data else {}
            parsed["archivo"] = await archivo.read()
            parsed["nombre_archivo"] = archivo.filename or "file"
        else:
            parsed = await request.json()
        return UpdateInventarioCommand(**parsed)
