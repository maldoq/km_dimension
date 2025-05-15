from fastapi import HTTPException
from sqlalchemy.orm import Session  # <-- Utilise SQLAlchemy ici
from app.models.fiche_calcul import FicheCalcul


def update_image_url(fiche_id: int, image_url: str, db: Session):
    fiche = db.query(FicheCalcul).filter(FicheCalcul.id == fiche_id).first()  # <-- Correction ici
    if not fiche:
        raise HTTPException(status_code=404, detail="Fiche non trouvée")

    fiche.image_url = image_url
    db.commit()
    db.refresh(fiche)
    return fiche
