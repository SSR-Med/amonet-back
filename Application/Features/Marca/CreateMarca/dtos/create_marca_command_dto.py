from pydantic import BaseModel


class CreateMarcaCommandDto(BaseModel):
    nombre: str
