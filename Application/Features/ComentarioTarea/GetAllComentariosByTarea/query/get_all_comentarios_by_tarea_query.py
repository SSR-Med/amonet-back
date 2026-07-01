from uuid import UUID

from pydantic import BaseModel


class GetAllComentariosByTareaQuery(BaseModel):
    amonet_tarea_sprint_id: UUID
