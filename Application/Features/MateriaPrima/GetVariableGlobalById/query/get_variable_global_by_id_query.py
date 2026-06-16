from uuid import UUID
from pydantic import BaseModel


class GetVariableGlobalByIdQuery(BaseModel):
    id: UUID
