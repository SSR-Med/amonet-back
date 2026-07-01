from uuid import UUID

from pydantic import BaseModel


class DeleteComentarioTareaCommand(BaseModel):
    id: UUID
