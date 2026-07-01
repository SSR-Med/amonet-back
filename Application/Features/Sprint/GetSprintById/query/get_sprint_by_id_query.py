from uuid import UUID

from pydantic import BaseModel


class GetSprintByIdQuery(BaseModel):
    id: UUID
