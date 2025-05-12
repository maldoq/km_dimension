from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.donnee_escalier import DonneesEscalierCreate, DonneesEscalierUpdate, DonneesEscalierRead, DonneesEscalierDetail
from app.crud import donnee_escalier as crud
from app.database import get_db
from app.auth import get_current_user  # assure-toi que ce dépendance fonctionne
from app.models.user import User

router = APIRouter(prefix="/donnees/escalier", tags=["DonneesEscalier"])


@router.post("/", response_model=DonneesEscalierRead)
def create(donnees: DonneesEscalierCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_donnees_escalier(db, donnees)


@router.get("/{donnees_id}", response_model=DonneesEscalierDetail)
def read_one(donnees_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_obj = crud.get_donnees_escalier(db, donnees_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return db_obj


@router.get("/", response_model=list[DonneesEscalierRead])
def read_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_all_donnees_escalier(db)


@router.put("/{donnees_id}", response_model=DonneesEscalierRead)
def update(donnees_id: int, donnees: DonneesEscalierUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_obj = crud.update_donnees_escalier(db, donnees_id, donnees)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return db_obj


@router.delete("/{donnees_id}")
def delete(donnees_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    obj = crud.delete_donnees_escalier(db, donnees_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return {"ok": True}
