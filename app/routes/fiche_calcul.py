from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.fiche_calcul import FicheCalcul
from app.database import get_db
from app.schemas.fiche_calcul import FicheCalculCreate, FicheCalculUpdate, FicheCalculResponse
from app.auth import get_current_user  # assure-toi que ce dépendance fonctionne
from app.models.user import User

router = APIRouter(prefix="/fiches", tags=["FicheCalcul"])


# 🔹 Create fiche
@router.post("/", response_model=FicheCalculResponse)
def create_fiche(
    fiche_data: FicheCalculCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fiche = FicheCalcul(**fiche_data.dict(), utilisateur_id=current_user.id)
    db.add(fiche)
    db.commit()
    db.refresh(fiche)
    return fiche


# 🔸 Get all fiches of the current user
@router.get("/", response_model=List[FicheCalculResponse])
def get_user_fiches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(FicheCalcul).filter(FicheCalcul.utilisateur_id == current_user.id).all()


# 🔹 Get one fiche
@router.get("/{fiche_id}", response_model=FicheCalculResponse)
def get_one_fiche(
    fiche_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fiche = db.query(FicheCalcul).filter(
        FicheCalcul.id == fiche_id,
        FicheCalcul.utilisateur_id == current_user.id
    ).first()
    if not fiche:
        raise HTTPException(status_code=404, detail="Fiche not found")
    return fiche


# 🔄 Update fiche
@router.put("/{fiche_id}", response_model=FicheCalculResponse)
def update_fiche(
    fiche_id: int,
    update_data: FicheCalculUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fiche = db.query(FicheCalcul).filter(
        FicheCalcul.id == fiche_id,
        FicheCalcul.utilisateur_id == current_user.id
    ).first()
    if not fiche:
        raise HTTPException(status_code=404, detail="Fiche not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(fiche, key, value)

    db.commit()
    db.refresh(fiche)
    return fiche


# ❌ Delete fiche
@router.delete("/{fiche_id}")
def delete_fiche(
    fiche_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fiche = db.query(FicheCalcul).filter(
        FicheCalcul.id == fiche_id,
        FicheCalcul.utilisateur_id == current_user.id
    ).first()
    if not fiche:
        raise HTTPException(status_code=404, detail="Fiche not found")

    db.delete(fiche)
    db.commit()
    return {"detail": "Fiche deleted successfully"}
