# routes/formule.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.formule import Formule
from app.models.fiche_calcul import FicheCalcul
from app.schemas.fiche_calcul import FicheCalculResponse
from app.schemas.formule import FormuleCreate, FormuleUpdate, FormuleResponse
from app.auth import get_current_user
from typing import List

router = APIRouter(prefix="/formules", tags=["Formules"])

@router.post("/", response_model=FormuleResponse)
def create_formule(formule: FormuleCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_formule = Formule(nom=formule.nom, image_url=formule.image_url)
    db.add(db_formule)
    db.commit()
    db.refresh(db_formule)
    return db_formule

@router.get("/", response_model=List[FormuleResponse])
def get_all_formules(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Formule).all()

# 🔹 Get one formule by ID
@router.post("/{formule_id}/fiche-auto")
def create_fiche_with_data(
    formule_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    formule = db.query(Formule).filter(Formule.id == formule_id).first()
    if not formule:
        raise HTTPException(status_code=404, detail="Formule non trouvée")

    fiche = FicheCalcul(
        titre=f"Fiche {formule.nom}",
        formule_id=formule.id,
        utilisateur_id=user.id
    )
    db.add(fiche)
    db.commit()
    db.refresh(fiche)

    nom_formule = formule.nom.lower().strip()
    donnees = None
    donnees_type = ""

    if "poutrelle" in nom_formule:
        from app.models.donnee_poutrelle import DonneesPoutrelle
        donnees = DonneesPoutrelle(fiche_id=fiche.id)
        db.add(donnees)
        donnees_type = "poutrelle"

    elif "poutre" in nom_formule:
        from app.models.donnee_poutre import DonneesPoutre
        donnees = DonneesPoutre(fiche_id=fiche.id)
        db.add(donnees)
        donnees_type = "poutre"

    elif "semelle" in nom_formule:
        from app.models.donnee_semelle import DonneesSemelle
        donnees = DonneesSemelle(fiche_id=fiche.id)
        db.add(donnees)
        donnees_type = "semelle"

    elif "poteau" in nom_formule:
        from app.models.donnee_poteau import DonneesPoteau
        donnees = DonneesPoteau(fiche_id=fiche.id)
        db.add(donnees)
        donnees_type = "poteau"

    elif "escalier" in nom_formule:
        from app.models.donnee_escalier import DonneesEscalier
        donnees = DonneesEscalier(fiche_id=fiche.id)
        db.add(donnees)
        donnees_type = "escalier"

    else:
        raise HTTPException(status_code=400, detail="Type de formule non pris en charge")

    db.commit()
    db.refresh(donnees)

    return {
        "fiche_id": fiche.id,
        "formule": formule.nom,
        "donnees_type": donnees_type,
        "donnees_id": donnees.id,
        "donnees": donnees.__dict__
    }

# 🔸 Update formule
@router.put("/{formule_id}", response_model=FormuleResponse)
def update_formule(formule_id: int, updated_data: FormuleUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    formule = db.query(Formule).filter(Formule.id == formule_id).first()
    if not formule:
        raise HTTPException(status_code=404, detail="Formule not found")

    formule.nom = updated_data.nom
    formule.image_url = updated_data.image_url  # ✅ Ajouté

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
