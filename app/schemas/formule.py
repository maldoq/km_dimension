from pydantic import BaseModel
from typing import Optional

class FormuleCreate(BaseModel):
    nom: str
    image_url: Optional[str] = None  # ✅ Ajouté

class FormuleUpdate(BaseModel):
    nom: str
    image_url: Optional[str] = None  # ✅ Ajouté

class FormuleResponse(BaseModel):
    id: int
    nom: str
    image_url: Optional[str] = None  # ✅ Ajouté

    class Config:
        orm_mode = True

