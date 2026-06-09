from pydantic import BaseModel


class CreateVariablesGlobalesCommand(BaseModel):
    nombre: str
