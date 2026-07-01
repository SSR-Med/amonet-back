from uuid import UUID

from pydantic import BaseModel


class DeleteSprintCommand(BaseModel):
    id: UUID
