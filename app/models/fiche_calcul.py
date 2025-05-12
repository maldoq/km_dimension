# models/fiche_calcul.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class FicheCalcul(Base):
    __tablename__ = "fichecalcul"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    formule_id = Column(Integer, ForeignKey("formule.id"))
    utilisateur_id = Column(Integer, ForeignKey("user.id"))
    resultat = Column(Text, nullable=True)
    date_creation = Column(DateTime, default=datetime.now(timezone.utc))

    formule = relationship("Formule", back_populates="fiches")
    utilisateur = relationship("User", back_populates="fiches")
    donnees_poutrelle = relationship("DonneesPoutrelle", back_populates="fiche", uselist=False)
    donnees_poutre = relationship("DonneesPoutre", back_populates="fiche", uselist=False)
    donnees_semelle = relationship("DonneesSemelle", back_populates="fiche", uselist=False)
    donnees_poteau = relationship("DonneesPoteau", back_populates="fiche", uselist=False)
    donnees_escalier = relationship("DonneesEscalier", back_populates="fiche", uselist=False)
