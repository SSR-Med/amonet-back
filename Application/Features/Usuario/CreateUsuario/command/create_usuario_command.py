from pydantic import BaseModel


class CreateUsuarioCommand(BaseModel):
    documento: str
    nombre: str
    password: str
    rol: str
