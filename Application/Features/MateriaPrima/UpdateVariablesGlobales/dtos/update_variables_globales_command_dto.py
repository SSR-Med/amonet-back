from uuid import UUID

from pydantic import BaseModel


class UpdateVariablesGlobalesCommandDto(BaseModel):
    id: UUID | None = None
    nombre: str
