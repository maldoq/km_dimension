from sqlalchemy.orm import Session
from app.models.donnee_poutrelle import DonneesPoutrelle
from app.schemas.donnee_poutrelle import DonneesPoutrelleCreate, DonneesPoutrelleUpdate


def create_donnees_poutrelle(db: Session, donnees: DonneesPoutrelleCreate):
    db_donnees = DonneesPoutrelle(**donnees.model_dump())
    db_donnees.calculer()
    db.add(db_donnees)
    db.commit()
    db.refresh(db_donnees)
    return db_donnees 


def get_donnees_poutrelle(db: Session, donnees_id: int):
    return db.query(DonneesPoutrelle).filter(DonneesPoutrelle.id == donnees_id).first()


def get_all_donnees_poutrelles(db: Session):
    return db.query(DonneesPoutrelle).all()


def update_donnees_poutrelle(db: Session, donnees_id: int, updates: DonneesPoutrelleUpdate):
    db_donnees = db.query(DonneesPoutrelle).filter(DonneesPoutrelle.id == donnees_id).first()
    if not db_donnees:
        return None

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_donnees, key, value)

    db_donnees.calculer()
    db.commit()
    db.refresh(db_donnees)
    return db_donnees


def delete_donnees_poutrelle(db: Session, donnees_id: int):
    db_donnees = db.query(DonneesPoutrelle).filter(DonneesPoutrelle.id == donnees_id).first()
    if db_donnees:
        db.delete(db_donnees)
        db.commit()
    return db_donnees
