from uuid import UUID

from pydantic import BaseModel


class GetColumnaKanbanByIdQuery(BaseModel):
    id: UUID
