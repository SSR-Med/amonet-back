from uuid import UUID

from pydantic import BaseModel


class GetTareasBySprintQuery(BaseModel):
    amonet_sprint_id: UUID
