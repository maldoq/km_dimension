from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FicheCalculCreate(BaseModel):
    titre: str
    formule_id: int
    resultat: Optional[str] = None

class FicheCalculUpdate(BaseModel):
    titre: Optional[str] = None
    formule_id: Optional[int] = None
    resultat: Optional[str] = None

class FicheCalculResponse(BaseModel):
    id: int
    titre: str
    image_url: Optional[str]
    formule_id: int
    utilisateur_id: int
    resultat: Optional[str]
    date_creation: datetime

    class Config:
        orm_mode = True
