import os
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from app.database import users_collection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "tyda-secret-key-2025")
ALGORITHM = "HS256"


# Hash & Verify
def hasher_mot_de_passe(mot_de_passe: str) -> str:
    return pwd_context.hash(mot_de_passe)


def verifier_mot_de_passe(mot_de_passe_simple: str, mot_de_passe_hashe: str) -> bool:
    return pwd_context.verify(mot_de_passe_simple, mot_de_passe_hashe)


# JWT
def creer_token_acces(donnees: dict, expires_delta: timedelta | None = None):
    donnees_a_encoder = donnees.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))
    donnees_a_encoder.update({"exp": expire})
    return jwt.encode(donnees_a_encoder, SECRET_KEY, algorithm=ALGORITHM)


async def obtenir_utilisateur_actuel(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token invalide")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalide")


# Rôles
def verifier_role(role_requis: str):
    async def wrapper(user_id: str = Depends(obtenir_utilisateur_actuel)):
        utilisateur = await users_collection.find_one({"user_id": user_id}, {"_id": 0})
        if not utilisateur or utilisateur.get("role") != role_requis:
            raise HTTPException(status_code=403, detail="Accès refusé")
        return utilisateur

    return wrapper
