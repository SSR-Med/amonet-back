from uuid import UUID

from pydantic import BaseModel


class DeletePrioridadKanbanCommand(BaseModel):
    id: UUID
