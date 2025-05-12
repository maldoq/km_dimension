from pydantic import BaseModel
from typing import Optional


class DonneesPoutreBase(BaseModel):
    fiche_id: int
    fc28: Optional[float]
    fe: Optional[float]
    g: Optional[float]
    q: Optional[float]
    lx: Optional[float]
    c: Optional[float] 
    h: Optional[float]
    b: Optional[float]


class DonneesPoutreCreate(DonneesPoutreBase):
    pass


class DonneesPoutreUpdate(DonneesPoutreBase):
    pass


class DonneesPoutreRead(DonneesPoutreBase):
    id: int

    class Config:
        orm_mode = True


class DonneesPoutreDetail(DonneesPoutreRead):
    gamma_b: float
    theta: float
    fbu: float
    fsu: float
    pu: float
    mu: float
    d: float
    µ: float
    alpha: float
    z: float
    As: float

    class Config:
        orm_mode = True
