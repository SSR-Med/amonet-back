from uuid import UUID

from pydantic import BaseModel


class DeleteColumnaKanbanCommand(BaseModel):
    id: UUID
