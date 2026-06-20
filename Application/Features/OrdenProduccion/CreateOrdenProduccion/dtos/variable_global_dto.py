from uuid import UUID

from pydantic import BaseModel


class VariableGlobalDto(BaseModel):
    amonet_variable_materia_prima_id: UUID
    cantidad: int
