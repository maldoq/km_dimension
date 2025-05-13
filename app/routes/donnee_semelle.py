from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import io
from app.utils.pdf_generator import generate_pdf_semelle
from app.schemas.donnee_semelle import DonneesSemelleCreate, DonneesSemelleUpdate, DonneesSemelleRead, DonneesSemelleDetail
from app.crud import donnee_semelle as crud
from app.database import get_db
from app.auth import get_current_user  # assure-toi que ce dépendance fonctionne
from app.models.user import User

router = APIRouter(prefix="/donnees/semelle", tags=["DonneesSemelle"])


@router.post("/", response_model=DonneesSemelleRead)
def create(donnees: DonneesSemelleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_donnees_semelle(db, donnees)


@router.get("/{donnees_id}", response_model=DonneesSemelleDetail)
def read_one(donnees_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_obj = crud.get_donnees_semelle(db, donnees_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return db_obj


@router.get("/", response_model=list[DonneesSemelleRead])
def read_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_all_donnees_semelle(db)


@router.put("/{donnees_id}", response_model=DonneesSemelleRead)
def update(donnees_id: int, donnees: DonneesSemelleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_obj = crud.update_donnees_semelle(db, donnees_id, donnees)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return db_obj


@router.delete("/{donnees_id}")
def delete(donnees_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    obj = crud.delete_donnees_semelle(db, donnees_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return {"ok": True}

@router.get("/{donnee_id}/pdf", response_class=StreamingResponse)
def generate_pdf(donnee_id: int, db: Session = Depends(get_db)):
    obj = crud.get_donnees_semelle(db, donnee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Donnée introuvable")

    pdf_content = generate_pdf_semelle(data=obj.__dict__)
    return StreamingResponse(io.BytesIO(pdf_content), media_type="application/pdf", headers={
        "Content-Disposition": f"inline; filename=donnee_semelle_{donnee_id}.pdf"
    })
