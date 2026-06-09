from uuid import UUID

from pydantic import BaseModel


class UpdateVariablesGlobalesCommand(BaseModel):
    id: UUID | None = None
    nombre: str
