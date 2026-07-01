from uuid import UUID

from pydantic import BaseModel


class GetTareaSprintByIdQuery(BaseModel):
    id: UUID
