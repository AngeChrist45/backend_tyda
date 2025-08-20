from pydantic import BaseModel
from typing import List


class Produit(BaseModel):
    nom: str
    description: str
    prix: float
    categorie: str
    stock: int
    images: List[str] = []
    tailles: List[str] = []
    couleurs: List[str] = []
    vendeur_id: str | None = None
    statut: str = "en_attente" # en_attente, accepte, refuse