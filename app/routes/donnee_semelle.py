from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import io
import os
import shutil
from app.utils.pdf_generator import generate_pdf_semelle
from app.schemas.donnee_semelle import DonneesSemelleCreate, DonneesSemelleUpdate, DonneesSemelleRead, DonneesSemelleDetail
from app.crud import donnee_semelle as crud
from app.database import get_db
from app.auth import get_current_user  # assure-toi que ce dépendance fonctionne
from app.models.user import User
from app.models.donnee_semelle import DonneesSemelle

router = APIRouter(prefix="/donnees/semelle", tags=["DonneesSemelle"])

UPLOAD_DIR = "static/images/donnees_semelle"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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

@router.post("/{semelle_id}/upload-image/")
def upload_image_semelle(semelle_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    semelle = db.query(DonneesSemelle).filter(DonneesSemelle.id == semelle_id).first()
    if not semelle:
        raise HTTPException(status_code=404, detail="semelle non trouvée.")

    filename = f"semelle_{semelle_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    semelle.image_url = f"/{file_path}"  # ou une URL publique selon ton setup
    db.commit()

    return {"message": "Image uploadée avec succès", "image_url": semelle.image_url}
