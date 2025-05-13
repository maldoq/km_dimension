from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base
import math as mt


class DonneesPoutre(Base):
    __tablename__ = "donneespoutre"

    id = Column(Integer, primary_key=True, index=True)
    fiche_id = Column(Integer, ForeignKey("fichecalcul.id"), unique=True)

    # Variables
    fc28 = Column(Float)
    fe = Column(Float)
    g = Column(Float)
    q = Column(Float)
    lx = Column(Float)
    c = Column(Float)
    h = Column(Float)
    b = Column(Float) 

    # Paramètres par défaut
    gamma_b = Column(Float, default=1.5)
    theta = Column(Float, default=1.0)

    # Variables calculées
    fbu = Column(Float)
    fsu = Column(Float)
    pu = Column(Float)
    mu = Column(Float)
    d = Column(Float)
    µ = Column(Float)
    alpha = Column(Float)
    z = Column(Float)
    As = Column(Float)

    fiche = relationship("FicheCalcul", back_populates="donnees_poutre")

    def calculer(self):
        if self.fc28 is None or self.fe is None or self.g is None or self.q is None or self.lx is None or self.c is None or self.h is None or self.b is None:
            raise ValueError("Certaines données nécessaires sont manquantes.")

        # Appliquer les valeurs par défaut manuellement si elles sont absentes
        theta = self.theta if self.theta is not None else 1.0
        gamma_b = self.gamma_b if self.gamma_b is not None else 1.5

        self.fbu = (0.85 * self.fc28) / (theta * gamma_b)
        self.fsu = self.fe / 1.15
        self.pu = 1.35 * self.g + 1.5 * self.q
        self.mu = (self.pu * self.lx ** 2) / 8
        self.d = self.h - self.c - 1
        self.µ = (self.mu * 10 ** 4) / (self.b * (self.d * 10 ** -2) ** 2 * self.fbu * 10 ** 6)
        self.alpha = 1.25 * (1 - mt.sqrt(1 - 2 * self.µ))
        self.z = (self.d * 10 ** -2) * (1 - 0.4 * self.alpha)
        self.As = (self.mu * 10 ** 4) / (self.fbu * 10 ** 6 * self.z)
        # Enregistrer les résultats dans la base de données

