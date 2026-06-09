from pydantic import BaseModel


class CreateMarcaCommand(BaseModel):
    nombre: str
