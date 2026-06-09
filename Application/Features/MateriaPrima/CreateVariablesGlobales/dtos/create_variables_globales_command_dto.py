from pydantic import BaseModel


class CreateVariablesGlobalesCommandDto(BaseModel):
    nombre: str
