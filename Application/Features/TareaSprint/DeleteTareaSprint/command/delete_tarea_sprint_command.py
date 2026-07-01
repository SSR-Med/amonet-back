from uuid import UUID

from pydantic import BaseModel


class DeleteTareaSprintCommand(BaseModel):
    id: UUID
