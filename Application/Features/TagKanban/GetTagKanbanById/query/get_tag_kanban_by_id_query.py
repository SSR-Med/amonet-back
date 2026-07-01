from uuid import UUID

from pydantic import BaseModel


class GetTagKanbanByIdQuery(BaseModel):
    id: UUID
