from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import io
import os
import shutil
from app.utils.pdf_generator import generate_pdf_poutre
from app.schemas.donnee_poutre import DonneesPoutreCreate, DonneesPoutreUpdate, DonneesPoutreRead, DonneesPoutreDetail
from app.crud import donnee_poutre as crud
from app.database import get_db
from app.auth import get_current_user  # assure-toi que ce dépendance fonctionne
from app.models.user import User
from app.models.donnee_poutre import DonneesPoutre

router = APIRouter(prefix="/donnees/poutre", tags=["DonneesPoutre"])

UPLOAD_DIR = "static/images/donnees_poutre"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=DonneesPoutreRead)
def create(donnees: DonneesPoutreCreate, db: Session = Depends(get_db)):
    return crud.create_donnees_poutre(db, donnees)


@router.get("/{donnees_id}", response_model=DonneesPoutreDetail)
def read_one(donnees_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_donnees_poutre(db, donnees_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return db_obj


@router.get("/", response_model=list[DonneesPoutreRead])
def read_all(db: Session = Depends(get_db)):
    return crud.get_all_donnees_poutres(db)


@router.put("/{donnees_id}", response_model=DonneesPoutreRead)
def update(donnees_id: int, donnees: DonneesPoutreUpdate, db: Session = Depends(get_db)):
    db_obj = crud.update_donnees_poutre(db, donnees_id, donnees)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return db_obj


@router.delete("/{donnees_id}")
def delete(donnees_id: int, db: Session = Depends(get_db)):
    obj = crud.delete_donnees_poutre(db, donnees_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return {"ok": True}

@router.get("/{donnee_id}/pdf", response_class=StreamingResponse)
def generate_pdf(donnee_id: int, db: Session = Depends(get_db)):
    obj = crud.get_donnees_poutre(db, donnee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Donnée introuvable")

    pdf_content = generate_pdf_poutre(data=obj.__dict__)
    return StreamingResponse(io.BytesIO(pdf_content), media_type="application/pdf", headers={
        "Content-Disposition": f"inline; filename=donnee_poutre_{donnee_id}.pdf"
    })

@router.post("/{poutre_id}/upload-image/")
def upload_image_poutre(poutre_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    poutre = db.query(DonneesPoutre).filter(DonneesPoutre.id == poutre_id).first()
    if not poutre:
        raise HTTPException(status_code=404, detail="Poutre non trouvée.")

    filename = f"poutre_{poutre_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    poutre.image_url = f"/{file_path}"  # ou une URL publique selon ton setup
    db.commit()

    return {"message": "Image uploadée avec succès", "image_url": poutre.image_url}
