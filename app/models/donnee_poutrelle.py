from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from app.database import Base
import math as mt


class DonneesPoutrelle(Base):
    __tablename__ = "donneespoutrelle"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=True)  # <--- CHAMP AJOUTÉ
    fiche_id = Column(Integer, ForeignKey("fichecalcul.id"), unique=True)

    g = Column(Float) # charge pemanente (décanewton par mètre)
    q = Column(Float) # charge d'exploitation (décanewton par mètre)
    l = Column(Float) # Longueur de la portée (en mètre)
    h0 = Column(Float) # Dalle de compression (en mètre)
    fc28 = Column(Float) # Résistance à la compression (en méga-pascal)
    h = Column(Float) # L'épaisseur de la dalle (en mètre)

    b = Column(Float, default=0.6)
    b0 = Column(Float, default=0.12)
    gamma_b = Column(Float, default=1.5)
    theta = Column(Float, default=1.0)
    fsu = Column(Float, default=347.83)

    elu = Column(Float) # combinaison de charges - état limite ultime (décanewton par mètre)
    els = Column(Float) # combinaison de charges - état limite de service (décanewton par mètre)
    moment_max_elu = Column(Float) # moment maximale elu (décanewton . mètre)
    moment_max_els = Column(Float) # moment maximale els (décanewton . mètre)
    tu = Column(Float) # effort tranchant pour elu (décanewton . mètre)
    ts = Column(Float) # effort tranchant pour els (décanewton . mètre)
    fbu = Column(Float) # (en méga-pascal)
    d = Column(Float) # (en mètre)
    mu_verif = Column(Float) # moment de résistance - comparaison  (décanewton . mètre)
    mue = Column(Float) # (pas d'unité)
    z = Column(Float) # (en mètre)
    alpha = Column(Float) # (pas d'unité)
    ast = Column(Float) # (mètre carré) vedette

    fiche = relationship("FicheCalcul", back_populates="donnees_poutrelle")

    def calculer(self):
        if self.g is None or self.q is None or self.l is None or self.fc28 is None or self.h is None or self.h0 is None:
            raise ValueError("Certaines données nécessaires sont manquantes.")

        # Appliquer les valeurs par défaut manuellement si elles sont absentes
        theta = self.theta if self.theta is not None else 1.0
        gamma_b = self.gamma_b if self.gamma_b is not None else 1.5
        b = self.b if self.b is not None else 0.6
        b0 = self.b0 if self.b0 is not None else 0.12
        fsu = self.fsu if self.fsu is not None else 347.83

        self.elu = 1.35 * self.g + 1.5 * self.q
        self.els = self.g + self.q
        self.moment_max_elu = (self.elu * self.l**2) / 8
        self.moment_max_els = (self.els * self.l**2) / 8
        self.tu = (self.elu * self.l) / 2
        self.ts = (self.els * self.l) / 2
        self.fbu = (0.85 * self.fc28) / (theta * gamma_b)
        self.d = 0.9 * self.h
        mu = self.moment_max_elu
        self.mu_verif = b * self.h0 * self.fbu * (10 ** 5) * (self.d - self.h0 / 2)
        self.mue = mu / (b * (self.d ** 2) * self.fbu * 10 ** 4)
        self.alpha = 1.25 * (1 - mt.sqrt(1 - 2 * self.mue))
        self.z = self.d * (1 - 0.4 * self.alpha)
        self.ast = ((mu * 10 ** -2) / (self.z * fsu * 10 ** 3))
