from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from app.database import Base
import math as mt


class DonneesPoutre(Base):
    __tablename__ = "donneespoutre"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=True)  # <--- CHAMP AJOUTÉ

    # Variables
    fc28 = Column(Float) # (en méga-pascal)
    fe = Column(Float) # (en méga-pascal)
    g = Column(Float) # charge pemanente (en tonne par mètre)
    q = Column(Float) # charge d'exploitation (en tonne par mètre)
    lx = Column(Float) # longueur de la poutre (en mètre)
    h = Column(Float) # hauteur de la poutre (en centimètre)
    b = Column(Float) # l'épaisseur de la poutre (en mètre)

    # Paramètres par défaut
    gamma_b = Column(Float, default=1.5)
    theta = Column(Float, default=1.0)

    # Variables calculées
    fbu = Column(Float) # illustre inconnu (en méga-pascal)
    fsu = Column(Float) # illustre inconnu (en méga-pascal)
    pu = Column(Float) # illustre inconnu (en tonne par mètre)
    mu = Column(Float) # moment ultime (en tonne par mètre)
    d = Column(Float) # (en mètre)
    µ = Column(Float) # (pas d'unité)
    alpha = Column(Float) # (pas d'unité)
    z = Column(Float) # (en mètre)
    As = Column(Float) # (en mètre carré)


    def calculer(self):
        if self.fc28 is None or self.fe is None or self.g is None or self.q is None or self.lx is None or self.h is None or self.b is None:
            raise ValueError("Certaines données nécessaires sont manquantes.")

        # Appliquer les valeurs par défaut manuellement si elles sont absentes
        theta = self.theta if self.theta is not None else 1.0
        gamma_b = self.gamma_b if self.gamma_b is not None else 1.5

        self.fbu = (0.85 * self.fc28) / (theta * gamma_b)
        self.fsu = self.fe / 1.15
        self.pu = 1.35 * self.g + 1.5 * self.q
        self.mu = (self.pu * self.lx ** 2) / 8
        self.d = 0.9 * self.h
        self.µ = (self.mu * 10 ** 4) / (self.b * self.d ** 2 * self.fbu * 10 ** 6)
        self.alpha = 1.25 * (1 - mt.sqrt(1 - 2 * self.µ))
        self.z = self.d * (1 - 0.4 * self.alpha)
        self.As = (self.mu * 10 ** 4) / (self.fsu * 10 ** 6 * self.z)
        # Enregistrer les résultats dans la base de données

