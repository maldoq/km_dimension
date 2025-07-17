from pydantic import BaseModel
from typing import Optional


class DonneesSemelleBase(BaseModel):
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
    gamma_s: Optional[float]
    ns: Optional[float]
    nu: Optional[float]
    Aa: Optional[float]
    Bb: Optional[float]
    d1: Optional[float]
    d2: Optional[float]
    d: Optional[float]
    h: Optional[float]
    h_metre: Optional[float]
    As__A: Optional[float]
    As__B: Optional[float]

    class Config:
        orm_mode = True
