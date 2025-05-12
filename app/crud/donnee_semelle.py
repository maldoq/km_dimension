from sqlalchemy.orm import Session
from app.models.donnee_semelle import DonneesSemelle
from app.schemas.donnee_semelle import DonneesSemelleBase, DonneesSemelleCreate, DonneesSemelleUpdate


def create_donnees_semelle(db: Session, donnees: DonneesSemelleCreate):
    db_donnees = DonneesSemelle(**donnees.model_dump())
    db_donnees.calculer()
    db.add(db_donnees)
    db.commit()
    db.refresh(db_donnees)
    return db_donnees 


def get_donnees_semelle(db: Session, donnees_id: int):
    return db.query(DonneesSemelle).filter(DonneesSemelle.id == donnees_id).first()


def get_all_donnees_semelle(db: Session):
    return db.query(DonneesSemelle).all()


def update_donnees_semelle(db: Session, donnees_id: int, updates: DonneesSemelleUpdate):
    db_donnees = db.query(DonneesSemelle).filter(DonneesSemelle.id == donnees_id).first()
    if not db_donnees:
        return None

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_donnees, key, value)

    db_donnees.calculer()
    db.commit()
    db.refresh(db_donnees)
    return db_donnees


def delete_donnees_semelle(db: Session, donnees_id: int):
    db_donnees = db.query(DonneesSemelle).filter(DonneesSemelle.id == donnees_id).first()
    if db_donnees:
        db.delete(db_donnees)
        db.commit()
    return db_donnees
