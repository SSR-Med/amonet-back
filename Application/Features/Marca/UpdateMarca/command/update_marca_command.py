from pydantic import BaseModel


class UpdateMarcaCommand(BaseModel):
    nombre: str
