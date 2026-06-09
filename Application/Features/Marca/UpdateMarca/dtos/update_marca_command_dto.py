from pydantic import BaseModel


class UpdateMarcaCommandDto(BaseModel):
    nombre: str
