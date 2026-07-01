from uuid import UUID

from pydantic import BaseModel


class UpdateColumnaKanbanCommand(BaseModel):
    nombre: str
    posicion: int
