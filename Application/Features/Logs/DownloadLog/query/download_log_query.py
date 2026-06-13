from pydantic import BaseModel


class DownloadLogQuery(BaseModel):
    nombre: str
