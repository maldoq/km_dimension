from pydantic import BaseModel
from typing import Optional


class DonneesPoutrelleBase(BaseModel):
    fiche_id: int
    g: Optional[float]
    q: Optional[float]
    l: Optional[float]
    h0: Optional[float]
    fc28: Optional[float]
    h: Optional[float]


class DonneesPoutrelleCreate(DonneesPoutrelleBase):
    pass


class DonneesPoutrelleUpdate(DonneesPoutrelleBase):
    pass


class DonneesPoutrelleRead(DonneesPoutrelleBase):
    id: int

    class Config:
        orm_mode = True


class DonneesPoutrelleDetail(DonneesPoutrelleRead):
    image_url: Optional[str]
    b: float
    b0: float
    gamma_b: float
    theta: float
    fsu: float
    elu: float
    els: float
    moment_max_elu: float
    moment_max_els: float
    pu: float
    ps: float
    tu: float
    ts: float
    fbu: float
    d: float
    mu_verif: float
    mue: float
    z: float
    alpha: float
    ast: float

    class Config:
        orm_mode = True
