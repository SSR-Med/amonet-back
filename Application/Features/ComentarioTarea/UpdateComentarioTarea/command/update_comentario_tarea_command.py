from pydantic import BaseModel


class UpdateComentarioTareaCommand(BaseModel):
    comentario: str
