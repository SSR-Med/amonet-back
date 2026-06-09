from pydantic import BaseModel


class UpdateVariablesGlobalesCommand(BaseModel):
    nombre: str
