from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from app.database import Base
import math as mt


class DonneesEscalier(Base):
    __tablename__ = "donneesescalier"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=True)  # <--- CHAMP AJOUTÉ
    fiche_id = Column(Integer, ForeignKey("fichecalcul.id"), unique=True)

    # Variables
    fc28 = Column(Float)  # Résistance à la compression (en méga-pascal)
    fe = Column(Float)  # Coefficient de résistance de l'acier (en méga-pascal)
    g1 = Column(Float)  # Charge permanente pour 1 mètre de palier (kN/ml)
    g2 = Column(Float)  # Charge permanente pour 1 mètre de volée (kN/ml)
    l = Column(Float)  # Épaisseur de la paillace (mètre)
    alpha = Column(Float)  # Angle que forme le mur et le sol pour l'escalier (degré)
    d = Column(Float)  # Illustre inconnu (centimètre)
    b = Column(Float)  # Illustre inconnu (centimètre)
    q = Column(Float)  # Charge d'exploitation (kN/ml)
    As_reel = Column(Float)  # Réel (centimètre carré par mètre linéaire)

    # Paramètres par défaut
    gamma_s = Column(Float, default=1.15)
    gamma_b = Column(Float, default=1.5)
    theta = Column(Float, default=1)

    # Variables calculées
    pu = Column(Float) # (kilonewton/ml (mètre linéaire))
    ps = Column(Float) # (kilonewton/ml (mètre linéaire))
    mu = Column(Float) # (kilonewton/ml (mètre linéaire))
    ms = Column(Float) # (kilonewton/ml (mètre linéaire))
    fbu = Column(Float) # (méga-pascal)
    fsu = Column(Float) # (méga-pascal)
    µ = Column(Float) # (pas d'unité)
    gamma = Column(Float) # (pas d'unité)
    µ_l1 = Column(Float) # (pas d'unité)
    alpha = Column(Float) # (pas d'unité)
    z = Column(Float) # (centimètre)
    As = Column(Float) # (centimètre carré par mètre linéaire)
    As_y = Column(Float) # (centimètre carré par mètre linéaire)
    As_c = Column(Float) # (centimètre carré par mètre linéaire)


    fiche = relationship("FicheCalcul", back_populates="donnees_escalier")

    def calculer(self):
        if self.fc28 is None or self.fe is None or self.g1 is None or self.g2 is None or self.l is None or self.alpha is None or self.d is None or self.b is None or self.q is None:
            raise ValueError("Certaines données nécessaires sont manquantes.")

        # Appliquer les valeurs par défaut manuellement si elles sont absentes
        gamma_s = self.gamma_s if self.gamma_s is not None else 1.15
        gamma_b = self.gamma_b if self.gamma_b is not None else 1.5
        theta = self.theta if self.theta is not None else 1

        self.pu = 1.35 * (self.g1 + self.g2) + 1.5 * self.q
        self.ps = self.g1 + self.g2 + self.q
        self.mu = (self.pu * self.l ** 2) / 8
        self.ms = (self.ps * self.l ** 2) / 8
        self.fbu = (0.85 * self.fc28) / (theta * gamma_b)
        self.fsu = self.fe / gamma_s
        self.µ = (self.mu * 10 ** 4) / (self.b * self.d ** 2 * self.fbu * 10)
        self.gamma = self.mu / self.ms
        self.μ_l1 = 0.322 * self.gamma + 5.1 * 10 ** -4 * self.fc28 - 0.31
        self.alpha = 1.25 * (1 - mt.sqrt(1 - 2 * self.µ))
        self.z = self.d * (1 - 0.4 * self.alpha)
        self.As = (self.mu * 10 ** 4) / (self.fsu * self.z * 10)
        self.As_y = self.As_reel / 4
        self.As_c = 0.15 * self.As_reel

        # Enregistrer les résultats dans la base de données

