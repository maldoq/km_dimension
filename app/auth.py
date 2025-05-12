# app/auth.py

from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from starlette import status
from jose import JWTError, jwt
from typing import List

from app.schemas.user import UserResponse
from app.database import SessionLocal
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# Schémas Pydantic
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    nom: str = Field(..., min_length=2)
    prenom: str = Field(..., min_length=2)
    contact: str = Field(..., pattern=r"^\+?[1-9]\d{7,14}$")

class Token(BaseModel):
    access_token: str
    token_type: str

# Dépendance pour la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Enregistrement
@router.post("/", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: db_dependency):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = User.hash_password(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        nom=user.nom,
        prenom=user.prenom,
        contact=user.contact
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

# Connexion
@router.post("/token", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(user.email, user.id, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

# Vérification et génération du token
def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.verify_password(password):
        return None
    return user

def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    payload = {
        "sub": email,
        "id": user_id,
        "exp": datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Récupération de l'utilisateur courant via token
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user_id = payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user  # <-- retourne l'objet User directement
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    

@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()
