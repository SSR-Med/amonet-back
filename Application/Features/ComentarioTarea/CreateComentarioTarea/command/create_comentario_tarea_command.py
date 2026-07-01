from uuid import UUID

from pydantic import BaseModel


class CreateComentarioTareaCommand(BaseModel):
    amonet_tarea_sprint_id: UUID
    comentario: str
