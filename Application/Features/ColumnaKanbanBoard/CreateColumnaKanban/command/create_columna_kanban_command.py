from pydantic import BaseModel


class CreateColumnaKanbanCommand(BaseModel):
    nombre: str
    posicion: int
