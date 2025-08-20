from fastapi import APIRouter, Depends, HTTPException
from app.services.security import obtenir_utilisateur_actuel
from app.database import users_collection

router = APIRouter()


@router.get("/profil")
async def obtenir_profil(user_id: str = Depends(obtenir_utilisateur_actuel)):
    utilisateur = await users_collection.find_one(
        {"user_id": user_id}, {"_id": 0, "mot_de_passe": 0}
    )
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    return {"utilisateur": utilisateur}
