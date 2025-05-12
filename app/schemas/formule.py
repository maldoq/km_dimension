from pydantic import BaseModel

class FormuleCreate(BaseModel):
    nom: str

class FormuleUpdate(BaseModel):
    nom: str

class FormuleResponse(BaseModel):
    id: int
    nom: str

    class Config:
        orm_mode = True

