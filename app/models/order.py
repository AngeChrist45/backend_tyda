from pydantic import BaseModel
from typing import List, Dict


class Commande(BaseModel):
    produits: List[Dict]
    acheteur_id: str
    montant_total: float
    adresse_livraison: str
    statut: str = "en_attente" # en_attente, validee, en_livraison, livree