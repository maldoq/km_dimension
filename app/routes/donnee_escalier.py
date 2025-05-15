from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import io
import os
import shutil
from app.utils.pdf_generator import generate_pdf_escalier
from app.schemas.donnee_escalier import DonneesEscalierCreate, DonneesEscalierUpdate, DonneesEscalierRead, DonneesEscalierDetail
from app.crud import donnee_escalier as crud
from app.database import get_db
from app.auth import get_current_user  # assure-toi que ce dépendance fonctionne
from app.models.user import User
from app.models.donnee_escalier import DonneesEscalier

router = APIRouter(prefix="/donnees/escalier", tags=["DonneesEscalier"])

UPLOAD_DIR = "static/images/donnees_escalier"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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

@router.get("/{donnee_id}/pdf", response_class=StreamingResponse)
def generate_pdf(donnee_id: int, db: Session = Depends(get_db)):
    obj = crud.get_donnees_escalier(db, donnee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Donnée introuvable")

    pdf_content = generate_pdf_escalier(data=obj.__dict__)
    return StreamingResponse(io.BytesIO(pdf_content), media_type="application/pdf", headers={
        "Content-Disposition": f"inline; filename=donnee_escalier_{donnee_id}.pdf"
    })

@router.post("/{escalier_id}/upload-image/")
def upload_image_escalier(escalier_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    escalier = db.query(DonneesEscalier).filter(DonneesEscalier.id == escalier_id).first()
    if not escalier:
        raise HTTPException(status_code=404, detail="Escalier non trouvée.")

    filename = f"escalier_{escalier_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    escalier.image_url = f"/{file_path}"  # ou une URL publique selon ton setup
    db.commit()

    return {"message": "Image uploadée avec succès", "image_url": escalier.image_url}
