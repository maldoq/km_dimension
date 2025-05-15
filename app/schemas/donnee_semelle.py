from pydantic import BaseModel
from typing import Optional


class DonneesSemelleBase(BaseModel):
    fiche_id: int
    a : Optional[float]
    b : Optional[float]
    g : Optional[float]
    q : Optional[float]
    cont_adm : Optional[float]
    fe : Optional[float]


class DonneesSemelleCreate(DonneesSemelleBase):
    pass


class DonneesSemelleUpdate(DonneesSemelleBase):
    pass


class DonneesSemelleRead(DonneesSemelleBase):
    id: int

    class Config:
        orm_mode = True


class DonneesSemelleDetail(DonneesSemelleRead):
    image_url: Optional[str]
    gamma_b: float
    gamma_s: float
    ns: float
    nu: float
    A: float
    B: float
    d1: float
    d2: float
    d: float
    h: float
    h_metre: float
    As__A: float
    As__B: float

    class Config:
        orm_mode = True
