from sqlalchemy.orm import Session
from app.models.donnee_poutre import DonneesPoutre
from app.schemas.donnee_poutre import DonneesPoutreBase, DonneesPoutreCreate, DonneesPoutreUpdate


def create_donnees_poutre(db: Session, donnees: DonneesPoutreCreate):
    db_donnees = DonneesPoutre(**donnees.model_dump())
    db_donnees.calculer()
    db.add(db_donnees)
    db.commit()
    db.refresh(db_donnees)
    return db_donnees 


def get_donnees_poutre(db: Session, donnees_id: int):
    return db.query(DonneesPoutre).filter(DonneesPoutre.id == donnees_id).first()


def get_all_donnees_poutres(db: Session):
    return db.query(DonneesPoutre).all()


def update_donnees_poutre(db: Session, donnees_id: int, updates: DonneesPoutreUpdate):
    db_donnees = db.query(DonneesPoutre).filter(DonneesPoutre.id == donnees_id).first()
    if not db_donnees:
        return None

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_donnees, key, value)

    db_donnees.calculer()
    db.commit()
    db.refresh(db_donnees)
    return db_donnees


def delete_donnees_poutre(db: Session, donnees_id: int):
    db_donnees = db.query(DonneesPoutre).filter(DonneesPoutre.id == donnees_id).first()
    if db_donnees:
        db.delete(db_donnees)
        db.commit()
    return db_donnees
