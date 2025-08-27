import uuid
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.user import UserRegister, UserLogin
from app.services.security import (
    hasher_mot_de_passe,
    verifier_mot_de_passe,
    creer_token_acces,
)
from app.database import users_collection

# Configurer les logs (au début du fichier ou dans main.py)
logging.basicConfig(
    level=logging.INFO,  # Niveau : DEBUG / INFO / WARNING / ERROR
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/inscription")
async def inscription(utilisateur: UserRegister):
    logger.info("📩 Nouvelle tentative d'inscription avec email=%s", utilisateur.email)

    utilisateur_existant = await users_collection.find_one({"email": utilisateur.email})
    if utilisateur_existant:
        logger.warning("⚠️ Email déjà utilisé : %s", utilisateur.email)
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

    logger.debug("🛠️ Utilisateur avant insertion: %s", nouveau_utilisateur)

    await users_collection.insert_one(nouveau_utilisateur)

    token = creer_token_acces({"sub": user_id})
    logger.info("✅ Inscription réussie pour email=%s", utilisateur.email)

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
