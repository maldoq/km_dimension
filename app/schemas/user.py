# schemas/user.py
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    nom: str
    prenom: str
    contact: str
    email: str

    class Config:
        orm_mode = True
