from pydantic import BaseModel
from typing import Optional


class DonneesEscalierBase(BaseModel):
    fiche_id: int
    fc28: Optional[float]
    fe: Optional[float]
    g1: Optional[float]
    g2: Optional[float]
    l: Optional[float]
    alpha: Optional[float]
    d: Optional[float]
    b: Optional[float]
    q: Optional[float]
    As_reel: Optional[float]


class DonneesEscalierCreate(DonneesEscalierBase):
    pass


class DonneesEscalierUpdate(DonneesEscalierBase):
    pass


class DonneesEscalierRead(DonneesEscalierBase):
    id: int

    class Config:
        orm_mode = True


class DonneesEscalierDetail(DonneesEscalierRead):
    image_url: Optional[str]
    gamma_b: float
    gamma_s: float
    theta: float
    ns: float
    pu: float
    ps: float
    mu: float
    ms: float
    fbu: float
    fsu: float
    µ: float
    gamma: float
    µ_l1: float
    alpha: float
    z: float
    As: float
    As_y: float
    As_c: float

    class Config:
        orm_mode = True
