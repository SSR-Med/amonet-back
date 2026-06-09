from uuid import UUID

from pydantic import BaseModel


class DeleteMarcaCommand(BaseModel):
    id: UUID
