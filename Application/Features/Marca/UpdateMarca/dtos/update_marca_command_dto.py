from uuid import UUID

from pydantic import BaseModel


class UpdateMarcaCommandDto(BaseModel):
    id: UUID | None = None
    nombre: str
