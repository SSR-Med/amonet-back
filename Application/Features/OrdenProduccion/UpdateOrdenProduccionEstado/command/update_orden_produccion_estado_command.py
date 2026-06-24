from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator


class UpdateOrdenProduccionEstadoCommand(BaseModel):
    amonet_estado_produccion_id: UUID
    cancel_razon_descripcion: Optional[str] = None

    @field_validator("cancel_razon_descripcion")
    @classmethod
    def trim_upper_cancel_reason(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        return v.strip().upper()
