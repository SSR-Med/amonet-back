from uuid import UUID

from pydantic import BaseModel


class DeleteProductoCommand(BaseModel):
    id: UUID
