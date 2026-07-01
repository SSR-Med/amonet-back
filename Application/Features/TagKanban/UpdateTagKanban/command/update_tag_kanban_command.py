from pydantic import BaseModel


class UpdateTagKanbanCommand(BaseModel):
    nombre: str
    color_red: int
    color_green: int
    color_blue: int
