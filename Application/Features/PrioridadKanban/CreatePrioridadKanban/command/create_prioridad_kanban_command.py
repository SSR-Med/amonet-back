from pydantic import BaseModel


class CreatePrioridadKanbanCommand(BaseModel):
    nombre: str
    color_red: int
    color_green: int
    color_blue: int
