from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base
import math as mt


class DonneesPoteau(Base):
    __tablename__ = "donneespoteau"

    id = Column(Integer, primary_key=True, index=True)
    fiche_id = Column(Integer, ForeignKey("fichecalcul.id"), unique=True)

    # Variables
    a = Column(Float)  # Largeur du poteau (centimètre)
    b = Column(Float)  # Longueur du poteau (centimètre)
    lf = Column(Float)  # Largeur d'influence (centimètre)
    nu = Column(Float)  # Charge à elu (tonne)
    fe = Column(Float)  # Coefficient de résistance de l'acier (en méga-pascal)
    fc28 = Column(Float)  # Résistance à la compression (en méga-pascal)

    # Paramètres par défaut
    gamma_s = Column(Float, default=1.15)
    gamma_b = Column(Float, default=1.5)

    # Variables calculées
    ns = Column(Float)
    I_min = Column(Float)  # Inertie minimale (centimètre exposant 4)
    Bb = Column(Float)  # Périmètre (centimètre carré)
    i = Column(Float)  # (centimètre)
    gamma = Column(Float)  # L'élancement (pas d'unité)
    alpha = Column(Float)  # (pas d'unité)
    Br = Column(Float)  # (pas d'unité)
    Ath = Column(Float)  # (centimètre carré)
    Ath_cent = Column(Float)  # (centimètre carré)
    u = Column(Float)  # (pas d'unité)
    A_4u = Column(Float)  # (centimètre carré)
    A_2_percent = Column(Float)  # (centimètre carré)
    A_min = Column(Float)  # (centimètre carré)
    A_5_percent = Column(Float)  # (centimètre carré)
    A_max = Column(Float)  # (centimètre carré)
    As_calc = Column(Float)  # (centimètre carré)


    fiche = relationship("FicheCalcul", back_populates="donnees_poteau")

    def calculer(self):
        if self.fc28 is None or self.fe is None or self.a is None or self.b is None or self.lf is None or self.nu is None:
            raise ValueError("Certaines données nécessaires sont manquantes.")

        # Appliquer les valeurs par défaut manuellement si elles sont absentes
        gamma_s = self.gamma_s if self.gamma_s is not None else 1.15
        gamma_b = self.gamma_b if self.gamma_b is not None else 1.5

        self.I_min = (self.b * self.a ** 3) / 12
        self.Bb = self.a * self.b
        self.i = mt.sqrt(self.I_min / self.Bb)
        self.gamma = self.lf / self.i
        if self.gamma <= 70:
            pass
        else:
            self.gamma = 2 * mt.sqrt(3) * (self.lf / self.a)
        if self.gamma <= 50:
            self.alpha = 0.85 / (1 + 0.2 * ((self.gamma / 35) ** 2))
        else:
            self.alpha = 0.6 * (50 / self.gamma) ** 2
        
        self.Br = (self.a - 2)  * (self.b - 2)
        self.Ath = (((self.nu * 10 ** -2) / self.alpha) - ((self.Br * 10 ** -4 * self.fc28) / (0.9 * gamma_b))) * (gamma_s / self.fe) * 10 ** 4
        self.Ath_cent = self.Ath * 10 ** 4
        self.u = (self.a * (10 ** -2) + self.b * (10 ** -2)) * 2
        self.A_4u = 4 * self.u
        self.A_2_percent = (0.2 * self.Bb) / 100
        self.A_min = max(self.A_4u,self.A_2_percent)
        self.A_5_percent = (5 * self.Bb) / 100
        self.A_max = self.A_5_percent
        self.As_calc = max(self.Ath_cent, self.A_min)


        # Enregistrer les résultats dans la base de données

