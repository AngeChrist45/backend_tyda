import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.models.product import Produit
from app.database import products_collection, users_collection, notifications_collection
from app.services.security import verifier_role

router = APIRouter()


@router.get("/produits")
async def obtenir_produits(categorie: Optional[str] = None, recherche: Optional[str] = None):
    filtre = {"statut": "accepte"}
    if categorie:
        filtre["categorie"] = categorie
    if recherche:
        filtre["$or"] = [
            {"nom": {"$regex": recherche, "$options": "i"}},
            {"description": {"$regex": recherche, "$options": "i"}},
        ]

    produits = await products_collection.find(filtre, {"_id": 0}).to_list(length=None)
    return {"produits": produits}


@router.post("/produits")
async def ajouter_produit(produit: Produit, vendeur: dict = Depends(verifier_role("vendeur"))):
    produit_id = str(uuid.uuid4())
    nouveau_produit = {
        "produit_id": produit_id,
        "nom": produit.nom,
        "description": produit.description,
        "prix": produit.prix,
        "categorie": produit.categorie,
        "stock": produit.stock,
        "images": produit.images,
        "tailles": produit.tailles,
        "couleurs": produit.couleurs,
        "vendeur_id": vendeur["user_id"],
        "statut": "en_attente",
        "date_creation": datetime.utcnow(),
    }

    # Sauvegarde du produit
    await products_collection.insert_one(nouveau_produit)

    # Notification admin (optionnel mais utile)
    notification = {
        "notification_id": str(uuid.uuid4()),
        "type": "nouveau_produit",
        "message": f"Nouveau produit en attente : {produit.nom}",
        "date_creation": datetime.utcnow(),
        "lu": False,
    }
    await notifications_collection.insert_one(notification)

    return {"message": "Produit ajouté avec succès, en attente de validation", "produit_id": produit_id}
