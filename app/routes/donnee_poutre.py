from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.donnee_poutre import DonneesPoutreCreate, DonneesPoutreUpdate, DonneesPoutreRead, DonneesPoutreDetail
from app.crud import donnee_poutre as crud
from app.database import get_db
from app.auth import get_current_user  # assure-toi que ce dépendance fonctionne
from app.models.user import User

router = APIRouter(prefix="/donnees/poutre", tags=["DonneesPoutre"])


@router.post("/", response_model=DonneesPoutreRead)
def create(donnees: DonneesPoutreCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_donnees_poutre(db, donnees)


@router.get("/{donnees_id}", response_model=DonneesPoutreDetail)
def read_one(donnees_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_obj = crud.get_donnees_poutre(db, donnees_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return db_obj


@router.get("/", response_model=list[DonneesPoutreRead])
def read_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_all_donnees_poutres(db)


@router.put("/{donnees_id}", response_model=DonneesPoutreRead)
def update(donnees_id: int, donnees: DonneesPoutreUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_obj = crud.update_donnees_poutre(db, donnees_id, donnees)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return db_obj


@router.delete("/{donnees_id}")
def delete(donnees_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    obj = crud.delete_donnees_poutre(db, donnees_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return {"ok": True}
