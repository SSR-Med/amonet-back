from uuid import UUID

from pydantic import BaseModel


class GetOrdenProduccionByIdQuery(BaseModel):
    id: UUID
