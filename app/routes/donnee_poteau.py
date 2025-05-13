from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import io
from app.utils.pdf_generator import generate_pdf_poteau
from app.schemas.donnee_poteau import DonneesPoteauCreate, DonneesPoteauUpdate, DonneesPoteauRead, DonneesPoteauDetail
from app.crud import donnee_poteau as crud
from app.database import get_db
from app.auth import get_current_user  # assure-toi que ce dépendance fonctionne
from app.models.user import User

router = APIRouter(prefix="/donnees/poteau", tags=["DonneesPoteau"])


@router.post("/", response_model=DonneesPoteauRead)
def create(donnees: DonneesPoteauCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_donnees_poteau(db, donnees)


@router.get("/{donnees_id}", response_model=DonneesPoteauDetail)
def read_one(donnees_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_obj = crud.get_donnees_poteau(db, donnees_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return db_obj


@router.get("/", response_model=list[DonneesPoteauRead])
def read_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_all_donnees_poteau(db)


@router.put("/{donnees_id}", response_model=DonneesPoteauRead)
def update(donnees_id: int, donnees: DonneesPoteauUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_obj = crud.update_donnees_poteau(db, donnees_id, donnees)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return db_obj


@router.delete("/{donnees_id}")
def delete(donnees_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    obj = crud.delete_donnees_poteau(db, donnees_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return {"ok": True}

@router.get("/{donnee_id}/pdf", response_class=StreamingResponse)
def generate_pdf(donnee_id: int, db: Session = Depends(get_db)):
    obj = crud.get_donnees_poteau(db, donnee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Donnée introuvable")

    pdf_content = generate_pdf_poteau(data=obj.__dict__)
    return StreamingResponse(io.BytesIO(pdf_content), media_type="application/pdf", headers={
        "Content-Disposition": f"inline; filename=donnee_poteau_{donnee_id}.pdf"
    })
