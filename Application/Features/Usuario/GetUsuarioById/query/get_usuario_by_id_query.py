from uuid import UUID
from pydantic import BaseModel


class GetUsuarioByIdQuery(BaseModel):
    id: UUID
