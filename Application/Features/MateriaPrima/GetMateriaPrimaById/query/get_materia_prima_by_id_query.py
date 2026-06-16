from uuid import UUID
from pydantic import BaseModel


class GetMateriaPrimaByIdQuery(BaseModel):
    id: UUID
