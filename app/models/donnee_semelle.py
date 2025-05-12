from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base
import math as mt


class DonneesSemelle(Base):
    __tablename__ = "donneessemelle"

    id = Column(Integer, primary_key=True, index=True)
    fiche_id = Column(Integer, ForeignKey("fichecalcul.id"), unique=True)

    # Variables
    a = Column(Float)
    b = Column(Float)
    g = Column(Float)
    q = Column(Float)
    cont_adm = Column(Float)
    fe = Column(Float)

    # Paramètres par défaut
    gamma_s = Column(Float, default=1.5)

    # Variables calculées
    ns = Column(Float)
    nu = Column(Float)
    Aa = Column(Float)
    Bb = Column(Float)
    d1 = Column(Float)
    d2 = Column(Float)
    d = Column(Float)
    h = Column(Float)
    h_metre = Column(Float)
    As__A = Column(Float)
    As__B = Column(Float)


    fiche = relationship("FicheCalcul", back_populates="donnees_semelle")

    # Fonction
    def arrondir_personnalise(x):
        n = int(x)  # partie entière de x
        if x < n + 0.5:
            return n + 0.5
        else:
            return n + 1

    def calculer(self):
        if self.a is None or self.b is None or self.g is None or self.q is None or self.cont_adm is None or self.fe is None:
            raise ValueError("Certaines données nécessaires sont manquantes.")

        # Appliquer les valeurs par défaut manuellement si elles sont absentes
        gamma_s = self.gamma_s if self.gamma_s is not None else 1.5

        self.ns = self.q + self.g
        self.nu = (1.35 * self.g) + (1.5 * self.q)
        self.Aa = mt.sqrt((self.a / self.b) * (self.ns / (self.cont_adm * 100)))
        self.Bb = mt.sqrt((self.b / self.a) * (self.ns / (self.cont_adm * 100)))
        self.Aa = self.arrondir_personnalise(self.A)
        self.Bb = self.arrondir_personnalise(self.Bb)
        self.d1 = (self.Aa - self.a) / 4
        self.d2 = (self.Bb - self.b) / 4
        self.d = max(self.d1, self.d2)
        self.h = (self.d * 10 ** 2) + 5
        self.h_metre = self.h / 100
        self.As__A = ((self.nu * (self.Aa - self.a)) / (8 * self.d * self.fe * 100)) * gamma_s
        self.As__B = ((self.nu * (self.Bb - self.b)) / (8 * self.d * self.fe * 100)) * gamma_s
        # Enregistrer les résultats dans la base de données

