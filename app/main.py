# app/main.py

from app import auth
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import database
from app.routes import formule, fiche_calcul, donnee_poutrelle, donnee_poutre, donnee_semelle, donnee_poteau, donnee_escalier

app = FastAPI()

# ✅ Crée les tables automatiquement au démarrage
database.Base.metadata.create_all(bind=database.engine)

app.include_router(auth.router)
app.include_router(formule.router)
app.include_router(fiche_calcul.router)
app.include_router(donnee_poutrelle.router)
app.include_router(donnee_poutre.router)
app.include_router(donnee_semelle.router)
app.include_router(donnee_poteau.router)
app.include_router(donnee_escalier.router)

# Exemple d'utilisation de la session DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"message": "Connexion SQLite OK"}
