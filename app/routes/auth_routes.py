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
    try:
        print("=== Début inscription ===")
        print(f"Payload reçu : {utilisateur.dict()}")

        # Vérifier si l'email existe déjà
        utilisateur_existant = await users_collection.find_one({"email": utilisateur.email})
        print(f"Utilisateur existant ? {utilisateur_existant is not None}")
        if utilisateur_existant:
            raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")

        # Création utilisateur
        user_id = str(uuid.uuid4())
        hashed_pwd = hasher_mot_de_passe(utilisateur.mot_de_passe)
        print("Mot de passe hashé avec succès")

        nouveau_utilisateur = {
            "user_id": user_id,
            "nom": utilisateur.nom,
            "prenom": utilisateur.prenom,
            "email": utilisateur.email,
            "telephone": utilisateur.telephone,
            "mot_de_passe": hashed_pwd,
            "role": utilisateur.role,
            "date_creation": datetime.utcnow(),
            "actif": True,
        }

        print("Insertion en base...")
        result = await users_collection.insert_one(nouveau_utilisateur)
        print(f"Résultat insertion : {result.inserted_id}")

        token = creer_token_acces({"sub": user_id})
        print("Token généré")

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

    except Exception as e:
        print("ERREUR pendant l'inscription :", str(e))
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")


@router.post("/connexion")
async def connexion(utilisateur: UserLogin):
    try:
        print("=== Début connexion ===")
        print(f"Payload reçu : {utilisateur.dict()}")

        utilisateur_db = await users_collection.find_one({"email": utilisateur.email})
        print(f"Utilisateur trouvé : {utilisateur_db is not None}")

        if not utilisateur_db:
            raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

        if not verifier_mot_de_passe(utilisateur.mot_de_passe, utilisateur_db["mot_de_passe"]):
            raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

        token = creer_token_acces({"sub": utilisateur_db["user_id"]})
        print("Connexion réussie, token généré")

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

    except Exception as e:
        print("ERREUR pendant la connexion :", str(e))
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")
