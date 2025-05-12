from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base
import math as mt


class DonneesPoutrelle(Base):
    __tablename__ = "donneespoutrelle"

    id = Column(Integer, primary_key=True, index=True)
    fiche_id = Column(Integer, ForeignKey("fichecalcul.id"), unique=True)

    g = Column(Float)
    q = Column(Float)
    l = Column(Float)
    h0 = Column(Float)
    fc28 = Column(Float)
    h = Column(Float)

    b = Column(Float, default=0.6)
    b0 = Column(Float, default=0.12)
    gamma_b = Column(Float, default=1.5)
    theta = Column(Float, default=1.0)
    fsu = Column(Float, default=347.83)

    elu = Column(Float)
    els = Column(Float)
    moment_max_elu = Column(Float)
    moment_max_els = Column(Float)
    pu = Column(Float)
    ps = Column(Float)
    tu = Column(Float)
    ts = Column(Float)
    fbu = Column(Float)
    d = Column(Float)
    mu_verif = Column(Float)
    mue = Column(Float)
    z = Column(Float)
    alpha = Column(Float)
    ast = Column(Float)

    fiche = relationship("FicheCalcul", back_populates="donnees_poutrelle")

    def calculer(self):
        if self.g is None or self.q is None or self.l is None or self.fc28 is None or self.h is None or self.h0 is None:
            raise ValueError("Certaines données nécessaires sont manquantes.")

        # Appliquer les valeurs par défaut manuellement si elles sont absentes
        theta = self.theta if self.theta is not None else 1.0
        gamma_b = self.gamma_b if self.gamma_b is not None else 1.5
        b = self.b if self.b is not None else 0.6
        fsu = self.fsu if self.fsu is not None else 347.83

        self.elu = 1.35 * self.g + 1.5 * self.q
        self.els = self.g + self.q
        self.pu = self.elu
        self.ps = self.els
        self.moment_max_elu = (self.pu * self.l**2) / 8
        self.moment_max_els = (self.ps * self.l**2) / 8
        self.tu = (self.pu * self.l) / 2
        self.ts = (self.ps * self.l) / 2
        self.fbu = (0.85 * self.fc28) / (theta * gamma_b)
        self.d = 0.9 * self.h
        mu = self.moment_max_elu
        self.mu_verif = b * self.h0 * self.fbu * (10 ** 5) * (self.d - self.h0 / 2)
        self.mue = mu / (b * (self.d ** 2) * self.fbu * 10 ** 4)
        self.alpha = 1.25 * (1 - mt.sqrt(1 - 2 * self.mue))
        self.z = self.d * (1 - 0.4 * self.alpha)
        self.ast = (mu * 10 ** -2) / (self.z * fsu * 10 ** 3)
