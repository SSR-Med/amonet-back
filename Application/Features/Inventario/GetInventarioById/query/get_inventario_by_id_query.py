from uuid import UUID

from pydantic import BaseModel


class GetInventarioByIdQuery(BaseModel):
    id: UUID
