from uuid import UUID

from pydantic import BaseModel


class DeleteUsuarioCommand(BaseModel):
    id: UUID
