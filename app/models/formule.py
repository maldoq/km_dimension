# models/formule.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Formule(Base):
    __tablename__ = "formule"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    image_url = Column(String, nullable=True)  # ✅ CHAMP AJOUTÉ

    fiches = relationship("FicheCalcul", back_populates="formule")

    def __str__(self):
        return self.nom
