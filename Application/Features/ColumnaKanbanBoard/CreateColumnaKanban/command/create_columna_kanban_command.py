from typing import Optional

from pydantic import BaseModel


class CreateColumnaKanbanCommand(BaseModel):
    nombre: str
    posicion: Optional[int] = None
