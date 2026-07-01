from uuid import UUID

from pydantic import BaseModel


class DeleteTagKanbanCommand(BaseModel):
    id: UUID
