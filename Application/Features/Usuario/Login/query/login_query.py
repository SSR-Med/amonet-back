from pydantic import BaseModel


class LoginQuery(BaseModel):
    documento: str
    password: str
