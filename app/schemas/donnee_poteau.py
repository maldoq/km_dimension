from pydantic import BaseModel
from typing import Optional


class DonneesPoteauBase(BaseModel):
    fiche_id: int
    a: Optional[float]
    b: Optional[float]
    lf: Optional[float]
    nu: Optional[float]
    fe: Optional[float]
    fc28: Optional[float]


class DonneesPoteauCreate(DonneesPoteauBase):
    pass


class DonneesPoteauUpdate(DonneesPoteauBase):
    pass


class DonneesPoteauRead(DonneesPoteauBase):
    id: int

    class Config:
        orm_mode = True


class DonneesPoteauDetail(DonneesPoteauRead):
    gamma_b: float
    gamma_s: float
    ns: float
    I_min: float
    B: float
    i: float
    gamma: float
    alpha: float
    Br: float
    Ath: float
    Ath_cent: float
    u: float
    A_4u: float
    A_2_percent: float
    A_min: float
    A_5_percent: float
    A_max: float
    As_calc: float

    class Config:
        orm_mode = True
