from typing import Optional

from pydantic import BaseModel


class UpdateColumnaKanbanCommand(BaseModel):
    nombre: Optional[str] = None
    posicion: Optional[int] = None
