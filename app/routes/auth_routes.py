import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.user import UserRegister, UserLogin
from app.services.security import (
    hasher_mot_de_passe,
    verifier_mot_de_passe,
    creer_token_acces,
)
from app.database import users_collection

router = APIRouter()


@router.post("/inscription")
async def inscription(utilisateur: UserRegister):
    utilisateur_existant = await users_collection.find_one({"email": utilisateur.email})
    if utilisateur_existant:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")

    user_id = str(uuid.uuid4())
    nouveau_utilisateur = {
        "user_id": user_id,
        "nom": utilisateur.nom,
        "prenom": utilisateur.prenom,
        "email": utilisateur.email,
        "telephone": utilisateur.telephone,
        "mot_de_passe": hasher_mot_de_passe(utilisateur.mot_de_passe),
        "role": utilisateur.role,
        "date_creation": datetime.utcnow(),
        "actif": True,
    }
    await users_collection.insert_one(nouveau_utilisateur)

    token = creer_token_acces({"sub": user_id})
    return {
        "message": "Inscription réussie",
        "token": token,
        "utilisateur": {
            "user_id": user_id,
            "nom": utilisateur.nom,
            "prenom": utilisateur.prenom,
            "email": utilisateur.email,
            "role": utilisateur.role,
        },
    }


@router.post("/connexion")
async def connexion(utilisateur: UserLogin):
    utilisateur_db = await users_collection.find_one({"email": utilisateur.email})
    if not utilisateur_db or not verifier_mot_de_passe(
        utilisateur.mot_de_passe, utilisateur_db["mot_de_passe"]
    ):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    token = creer_token_acces({"sub": utilisateur_db["user_id"]})
    return {
        "message": "Connexion réussie",
        "token": token,
        "utilisateur": {
            "user_id": utilisateur_db["user_id"],
            "nom": utilisateur_db["nom"],
            "prenom": utilisateur_db["prenom"],
            "email": utilisateur_db["email"],
            "role": utilisateur_db["role"],
        },
    }
