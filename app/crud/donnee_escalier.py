from sqlalchemy.orm import Session
from app.models.donnee_escalier import DonneesEscalier
from app.schemas.donnee_escalier import DonneesEscalierBase, DonneesEscalierCreate, DonneesEscalierUpdate


def create_donnees_escalier(db: Session, donnees: DonneesEscalierCreate):
    db_donnees = DonneesEscalier(**donnees.model_dump())
    db_donnees.calculer()
    db.add(db_donnees)
    db.commit()
    db.refresh(db_donnees)
    return db_donnees 


def get_donnees_escalier(db: Session, donnees_id: int):
    return db.query(DonneesEscalier).filter(DonneesEscalier.id == donnees_id).first()


def get_all_donnees_escalier(db: Session):
    return db.query(DonneesEscalier).all()


def update_donnees_escalier(db: Session, donnees_id: int, updates: DonneesEscalierUpdate):
    db_donnees = db.query(DonneesEscalier).filter(DonneesEscalier.id == donnees_id).first()
    if not db_donnees:
        return None

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_donnees, key, value)

    db_donnees.calculer()
    db.commit()
    db.refresh(db_donnees)
    return db_donnees


def delete_donnees_escalier(db: Session, donnees_id: int):
    db_donnees = db.query(DonneesEscalier).filter(DonneesEscalier.id == donnees_id).first()
    if db_donnees:
        db.delete(db_donnees)
        db.commit()
    return db_donnees
