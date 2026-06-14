from pydantic import BaseModel


class DownloadEvidenciaQuery(BaseModel):
    numero_ingreso: str
