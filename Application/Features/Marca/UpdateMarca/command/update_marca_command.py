from uuid import UUID

from pydantic import BaseModel


class UpdateMarcaCommand(BaseModel):
    id: UUID | None = None
    nombre: str
