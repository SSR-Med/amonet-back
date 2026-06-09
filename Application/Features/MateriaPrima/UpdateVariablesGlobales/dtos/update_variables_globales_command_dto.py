from pydantic import BaseModel


class UpdateVariablesGlobalesCommandDto(BaseModel):
    nombre: str
