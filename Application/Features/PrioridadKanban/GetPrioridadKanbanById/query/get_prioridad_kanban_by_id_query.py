from uuid import UUID

from pydantic import BaseModel


class GetPrioridadKanbanByIdQuery(BaseModel):
    id: UUID
