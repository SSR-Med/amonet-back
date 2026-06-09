from uuid import UUID

from pydantic import BaseModel


class DeleteVariablesGlobalesCommand(BaseModel):
    id: UUID
