from pydantic import BaseModel


class Logeduser(BaseModel):
    email:str
    password:str