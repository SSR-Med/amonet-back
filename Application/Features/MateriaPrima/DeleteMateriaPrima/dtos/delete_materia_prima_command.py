from uuid import UUID

from pydantic import BaseModel


class DeleteMateriaPrimaCommand(BaseModel):
    id: UUID
