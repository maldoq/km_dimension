# routes/formule.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.formule import Formule
from app.schemas.formule import FormuleCreate, FormuleUpdate, FormuleResponse
from app.auth import get_current_user
from typing import List

router = APIRouter(prefix="/formules", tags=["Formules"])

@router.post("/", response_model=FormuleResponse)
def create_formule(formule: FormuleCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_formule = Formule(nom=formule.nom)
    db.add(db_formule)
    db.commit()
    db.refresh(db_formule)
    return db_formule

@router.get("/", response_model=List[FormuleResponse])
def get_all_formules(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Formule).all()

# 🔹 Get one formule by ID
@router.get("/{formule_id}", response_model=FormuleResponse)
def get_formule(formule_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    formule = db.query(Formule).filter(Formule.id == formule_id).first()
    if not formule:
        raise HTTPException(status_code=404, detail="Formule not found")
    return formule

# # 🔸 Get info of one formule and create automatically a fiche
# @router.get("/{formule_id}/fiche", response_model=FormuleResponse)
# def get_formule_fiche(formule_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
#     formule = db.query(Formule).filter(Formule.id == formule_id).first()
#     if not formule:
#         raise HTTPException(status_code=404, detail="Formule not found")
    
#     # Here you would implement the logic to create a fiche automatically
#     # For now, we just return the formule
#     return formule

# 🔸 Update formule
@router.put("/{formule_id}", response_model=FormuleResponse)
def update_formule(formule_id: int, updated_data: FormuleUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    formule = db.query(Formule).filter(Formule.id == formule_id).first()
    if not formule:
        raise HTTPException(status_code=404, detail="Formule not found")
    formule.nom = updated_data.nom
    db.commit()
    db.refresh(formule)
    return formule

# ❌ Delete formule
@router.delete("/{formule_id}")
def delete_formule(formule_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    formule = db.query(Formule).filter(Formule.id == formule_id).first()
    if not formule:
        raise HTTPException(status_code=404, detail="Formule not found")
    db.delete(formule)
    db.commit()
    return {"detail": "Formule deleted successfully"}
