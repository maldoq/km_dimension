# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.database import Base
from passlib.context import CryptContext
from sqlalchemy.orm import relationship


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    role = Column(String, default="client")

    # Relation avec FicheCalcul
    fiches = relationship("FicheCalcul", back_populates="utilisateur")

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    def hash_password(password: str):
        return pwd_context.hash(password)
